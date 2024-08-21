import fitz
import re
import random
from os import path, makedirs

PHONE_NUMBER_REGEX = r"\b\d[\d\s]{4,15}\b"

# Can validate a email if email is passed
EMAIL_REGEX = r"^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$"
# Can detect a email from a line of text but creates subgroups
EMAIL_REGEX_V2 = r"\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*"
# Perfect
EMAIL_REGEX_V3 = r"\w+(?:[-+.']\w+)*@\w+(?:[-.]\w+)*\.\w+(?:[-.]\w+)*"


class SensihidePDF:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def extract_text_from_pdf(self):
        self.pdf_document = fitz.open(self.pdf_path)
        pdf_text = ""
        for page_num in range(len(self.pdf_document)):
            page = self.pdf_document[page_num]
            pdf_text += page.get_text()
        return pdf_text

    def find_sensitive_info(self, pdf_text):
        text_lines = pdf_text.split("\n")

        sensitive_founds = {
            "phone_numbers": [],
            "emails": []
        }

        for line in text_lines:
            phone_numbers = re.findall(PHONE_NUMBER_REGEX, line)
            emails = re.findall(EMAIL_REGEX_V3, line)

            if phone_numbers:
                sensitive_founds["phone_numbers"].append(*phone_numbers)
            if emails:
                sensitive_founds["emails"].append(*emails)

        if len(sensitive_founds["phone_numbers"]) == 0 and len(sensitive_founds["emails"]) == 0:
            return False, None

        return True, sensitive_founds

    def generate_cleaned_file(self, sensitive_info, output_path):
        output_dir = path.dirname(output_path)
        if not path.exists(output_dir):
            makedirs(output_dir)

        for page_num in range(len(self.pdf_document)):
            page = self.pdf_document[page_num]
            for phone_number_item in sensitive_info["phone_numbers"]:
                areas = page.search_for(phone_number_item)
                for area in areas:
                    page.add_redact_annot(area, fill=(0, 0, 0))
                    page.apply_redactions()

            for email_item in sensitive_info["emails"]:
                areas = page.search_for(email_item)
                for area in areas:
                    page.add_redact_annot(area, fill=(0, 0, 0))
                    page.apply_redactions()

        self.pdf_document.save(output_path)


fileObj = SensihidePDF("./resume.pdf")
pdf_text = fileObj.extract_text_from_pdf()
containes_sensitive_data, sensitive_info = fileObj.find_sensitive_info(
    pdf_text)

if not containes_sensitive_data:
    print("No sensitive data found in the pdf")
    exit(0)

input_file_name = path.splitext(path.basename(fileObj.pdf_path))[0]
output_file_path = f"./out/{input_file_name}-{
    str(random.randint(10000, 99999))}.pdf"
fileObj.generate_cleaned_file(sensitive_info, output_file_path)
print("Sensitive data has been removed from the pdf")
print(f"Output file path: {output_file_path}")
