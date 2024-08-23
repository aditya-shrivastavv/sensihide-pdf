resource "random_id" "pdf_redaction" {
  byte_length = 2
}

module "redact_pdf" {
  source = "./redact-pdf"

  project_id = var.project_id
  region     = var.region
  suffix     = random_id.pdf_redaction.hex
  credentials_json = var.credentials_json
}