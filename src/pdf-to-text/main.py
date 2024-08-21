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
    output_bucket = req["output_bucket"]
    output_folder = req["output_folder"]

    try:
        text_data = extract_text_from_pdf(input_file_bucket, input_file)
    except Exception as e:
        return {"error": f"Error extracting text from PDF: {str(e)}"}, 500

    try:
        save_text_to_bucket(text_data, output_bucket, output_folder)
    except Exception as e:
        return {"error": f"Error saving text to bucket: {str(e)}"}, 500

    return {
        "status": 200,
        "message": "Text extracted and saved successfully",
        "data": text_data
    }


def remove_temp_files(*files):
    for file in files:
        os.remove(file)


def extract_text_from_pdf(input_bucket, input_file):
    print(f"Downloading file: gs://{input_bucket}/{input_file}")

    in_bucket = storage_client.get_bucket(input_bucket)
    blob = in_bucket.get_blob(input_file)
    downloaded_filename = str(uuid.uuid4())
    blob.download_to_filename(downloaded_filename)

    print(f"Input file downloaded from bucket to: {downloaded_filename}")

    pdf_document = fitz.open(downloaded_filename)
    pdf_text = ""
    for page_num in range(len(pdf_document)):
        pdf_text += pdf_document[page_num].get_text()

    # Clean up the temporary files
    remove_temp_files(downloaded_filename)

    return pdf_text


def save_text_to_bucket(text_data, output_bucket, output_folder):
    # Save `pdf_text` to a temporary file
    text_filename = f"/tmp/{str(uuid.uuid4())}.txt"
    with open(text_filename, "w") as text_file:
        text_file.write(text_data)

    print(f"Extracted text saved to: {text_filename}")

    # Upload the temporary file to the output bucket
    out_bucket = storage_client.get_bucket(output_bucket)
    uploaded_filename = f"{output_folder}/{text_filename}"
    blob = out_bucket.blob(uploaded_filename)
    blob.upload_from_filename(text_filename)

    print(f"Text file uploaded to: gs://{output_bucket}/{uploaded_filename}")

    # Clean up the temporary files
    remove_temp_files(text_filename)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
