import os

from flask import Flask, request, jsonify
from google.cloud import storage
from google.cloud import bigquery

app = Flask(__name__)

BQ_DATASET = os.getenv("BQ_DATASET")
BQ_TABLE = os.getenv("BQ_TABLE")

if not BQ_DATASET:
    raise Exception("Missing BQ_DATASET environment variable")
if not BQ_TABLE:
    raise Exception("Missing BQ_TABLE environment variable")

storage_client = storage.Client()
bq_client = bigquery.Client()


@app.route("/", methods=["POST"])
def post_handler():
    req = request.get_json()
    findings = req["findings"]
    project_id = req["project_id"]

    try:
        result = write_to_bigquery(findings, project_id)
        return jsonify(result)
    except Exception as e:
        print(f"error: {e}")
        return ("", 500)


def write_to_bigquery(findings, project_id):
    full_table_name = f"{project_id}.{BQ_DATASET}.{BQ_TABLE}"
    bq_result = bq_client.insert_rows_json(
        table=full_table_name, json_rows=findings, ignore_unknown_values=True)

    # Check if write was successful
    if len(bq_result) == 0:
        print(f"Findings inserted in BQ table: {full_table_name}")
    else:
        print(f"BQ insert errors: {bq_result}")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
