import json
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
    print(req)
