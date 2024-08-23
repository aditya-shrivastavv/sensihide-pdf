import json
from flask import Flask, request, jsonify
import google.cloud.dlp

app = Flask(__name__)

dlp_client = google.cloud.dlp_v2.DlpServiceClient()


@app.route("/", methods=["POST"])
def post_handler():
    req = request.get_json()
    text_data = req["text_data"]
    dlp_template = req["dlp_template"]
    project_id = req["project_id"]

    print("Sending text to DLP API.")
    try:
        findings = run_dlp_on_text(text_data, dlp_template, project_id)
        return jsonify(findings)
    except Exception as e:
        print(f"Error processing text: {str(e)}")
        return {"error": f"Error processing text: {str(e)}"}, 500


def run_dlp_on_text(text_data, dlp_template, project_id):

    parent = f"projects/{project_id}"
    inspect_template = dlp_client.get_inspect_template(name=dlp_template)

    dlp_response = dlp_client.inspect_content(
        request={
            "parent": parent,
            "inspect_template_name": inspect_template.name,
            "item": {
                "value": text_data
            }
        }
    )
    print("DLP API response received: ", dlp_response.result)
    return json.dumps(dlp_response.result)
