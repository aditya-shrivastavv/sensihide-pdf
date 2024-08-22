import fitz
import os
import uuid
from flask import Flask, request
from google.cloud import storage

app = Flask(__name__)

storage_client = storage.Client()


@app.route("/", methods=["POST"])
def post_handler():
    req = request.get_json()

    input_file = req["input_file"]
    input_file_bucket = req["input_file_bucket"]
    buffer_bucket = req["buffer_bucket"]

    text_data = ""
    try:
        text_data = extract_text_from_pdf(input_file_bucket, input_file)
    except Exception as e:
        return {"error": f"Error extracting text from PDF: {str(e)}"}, 500

    text_filepath = ""
    try:
        text_filepath = save_text_to_bucket(text_data, buffer_bucket)
    except Exception as e:
        return {"error": f"Error saving text to bucket: {str(e)}"}, 500

    return {
        "status": 200,
        "message": "Text extracted and saved successfully",
        "data": text_filepath
    }


def remove_temp_files(*files):
    for file in files:
        os.remove(file)


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
    remove_temp_files(download_input_filename)

    return pdf_text


def save_text_to_bucket(text_data, buffer_bucket):
    # Save `pdf_text` to a temporary file
    text_filepath = f"/tmp/{str(uuid.uuid4())}.txt"
    with open(text_filepath, "w") as text_file:
        text_file.write(text_data)

    print(f"Extracted text saved to: {text_filepath}")

    # Upload the temporary file to the buffer bucket
    buffer_bucket_client = storage_client.get_bucket(buffer_bucket)
    blob = buffer_bucket_client.blob(text_filepath)
    blob.upload_from_filename(text_filepath)

    print(f"Text file uploaded to: gs://{buffer_bucket}/{text_filepath}")

    # Clean up the temporary files
    remove_temp_files(text_filepath)

    return text_filepath


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
