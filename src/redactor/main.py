import fitz
import os
import json
from flask import Flask, request, jsonify
from google.cloud import storage

app = Flask(__name__)

storage_client = storage.Client()


@app.route("/", methods=["POST"])
def post_handler():
    req = request.get_json()
    input_file = req["input_file"]
    input_file_bucket = req["input_file_bucket"]
    findings_data = req["findings"]
    output_bucket = req["output_bucket"]
    if not findings_data:
        return jsonify({"error": "No findings data provided"}), 400

    print("Findings data type: ", type(findings_data))
    findings = json.loads(findings_data)
    sensitive_text = get_quotes(findings)
    output_file = f"{input_file}_redacted.pdf"

    try:
        print("Downloading input file: ", input_file)
        download_input_file(input_file, input_file_bucket)

        print("Applying redactions")
        apply_redactions(input_file, sensitive_text, output_file)

        print("Uploading redacted file: ", output_file)
        upload_redacted_file(output_file, output_bucket)

        print("Redacted file uploaded successfully")

        return jsonify({"message": "Redacted file uploaded successfully"}), 200
    except Exception as e:
        print("Error applying redactions: ", e)
        return jsonify({"error": "Error applying redactions"}), 500


def get_quotes(findings_data):
    quotes = []
    for finding in findings_data["findings"]:
        quotes.append((finding["quote"], finding["infoType"]["name"]))
    return quotes


def download_input_file(input_file, input_file_bucket):
    bucket = storage_client.bucket(input_file_bucket)
    blob = bucket.blob(input_file)
    blob.download_to_filename(input_file)


def apply_redactions(input_file, sensitive_text, output_file):
    pdf_document = fitz.open(input_file)
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        for quote, quoteType in sensitive_text:
            areas = page.search_for(quote)
            for area in areas:
                page.add_redact_annot(area, text=f"[{quoteType}]", fill=(
                    0.8, 0.8, 0.8), fontsize=100)
                page.apply_redactions()

    pdf_document.save(output_file)


def upload_redacted_file(output_file, output_bucket):
    bucket = storage_client.bucket(output_bucket)
    blob = bucket.blob(output_file)
    blob.upload_from_filename(output_file)

    os.remove(output_file)
