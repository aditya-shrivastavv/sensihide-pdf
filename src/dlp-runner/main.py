import datetime
import json
import os
import uuid
from flask import Flask, request, jsonify
from google.cloud import storage
import google.cloud.dlp
import proto

app = Flask(__name__)


dlp_client = google.cloud.dlp_v2.DlpServiceClient()
storage_client = storage.Client()


@app.route("/", methods=["POST"])
def post_handler():
    req = request.get_json()
    input_file = req["input_file"]
    input_file_bucket = req["input_file_bucket"]
    dlp_template = req["dlp_template"]
    project_id = req["project_id"]

    try:
        findings = run_dlp_on_text(
            input_file, input_file_bucket, project_id, dlp_template)
        return jsonify(findings)
    except Exception as e:
        print(f"Error processing text: {str(e)}")
        return {"error": f"Error processing text: {str(e)}"}, 500


def run_dlp_on_text(input_file, input_file_bucket, project_id, inspect_template):

    # download file from bucket
    print(f"Downloading input file from gs://{input_file_bucket}/{input_file}")
    input_bucket_client = storage_client.get_bucket(input_file_bucket)
    blob = input_bucket_client.get_blob(input_file)
    blob.download_to_filename(input_file)
    print(f"Input file downloaded from GCS to: {input_file}")

    # redact file using DLP
    findings = get_findings(project_id, input_file, inspect_template)

    # delete file
    os.remove(input_file)

    return findings


def get_findings(project_id, input_file, inspect_template):
    file_content = ""
    with open(input_file, "r") as f:
        file_content = f.read()

    parent = f"projects/{project_id}"
    inspect_template = dlp_client.get_inspect_template(name=inspect_template)

    response = dlp_client.inspect_content(
        request={
            "parent": parent,
            "inspect_template_name": inspect_template.name,
            "item": {
                "value": file_content
            },
        }
    )

    return response.result
