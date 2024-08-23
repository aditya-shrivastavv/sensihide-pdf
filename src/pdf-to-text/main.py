import fitz
import os
import uuid
from flask import Flask, request, jsonify
from google.cloud import storage

app = Flask(__name__)

storage_client = storage.Client()


@app.route("/", methods=["POST"])
def post_handler():
    req = request.get_json()

    input_file = req["input_file"]
    input_file_bucket = req["input_file_bucket"]

    text_data = ""
    try:
        text_data = extract_text_from_pdf(input_file_bucket, input_file)
    except Exception as e:
        return {"error": f"Error extracting text from PDF: {str(e)}"}, 500

    return text_data


def extract_text_from_pdf(input_file_bucket, input_file):
    print(f"Downloading file: gs://{input_file_bucket}/{input_file}")

    input_bucket_client = storage_client.get_bucket(input_file_bucket)
    blob = input_bucket_client.get_blob(input_file)

    download_input_filename = str(uuid.uuid4())
    blob.download_to_filename(download_input_filename)

    print(f"Input file downloaded from bucket to: {download_input_filename}")

    pdf_document = fitz.open(download_input_filename)
    pdf_text = ""
    for page_num in range(len(pdf_document)):
        pdf_text += pdf_document[page_num].get_text()

    # Clean up the temporary files
    os.remove(download_input_filename)

    return jsonify(pdf_text)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
