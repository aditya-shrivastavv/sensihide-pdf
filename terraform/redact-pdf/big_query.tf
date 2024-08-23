resource "google_bigquery_dataset" "redact_pdf" {
  dataset_id    = "redact_pdf${local.app_suffix_underscore}"
  location      = var.region
  friendly_name = "Redact PDF Dataset"
  description   = "Dataset for storing data related to Redact PDF application"

  depends_on = [module.project_services]
}

resource "google_bigquery_table" "findings" {
  dataset_id          = google_bigquery_dataset.redact_pdf.dataset_id
  table_id            = "findings"
  deletion_protection = false
  schema              = templatefile("${path.module}/templates/big-query-table-findings.json", {})

  depends_on = [module.project_services]
}