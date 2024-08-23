import json
import os
from google.cloud.workflows import executions_v1beta

WORKFLOW_ID = os.getenv("WORKFLOW_ID", "")

if not WORKFLOW_ID:
    raise Exception("Missing required environment variable WORKFLOW_ID")

wf_exec_client = executions_v1beta.ExecutionsClient()


def handler(event, context):
    arguments = {
        "bucket": event["bucket"],
        "file": event["name"]
    }

    print(f"Recieved file: {arguments['file']
                            }, from bucket: {arguments['bucket']}")

    print(json.dumps(arguments))

    # Trigger the workflow
    wf_exec = wf_exec_client.create_execution(
        request={
            "parent": WORKFLOW_ID,
            "execution": {
                "argument": json.dumps(arguments)
            }
        }
    )

    print(f"Execution created: {wf_exec.name}")
