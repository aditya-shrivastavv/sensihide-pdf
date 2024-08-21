# PDF to Text

Flask server listening for POST requests on `/` route with a PDF file. The server download the PDF file from **input storage bucket** then extracts text data from it and saves the text data to a file and uploads that file to **output storage bucket**.
