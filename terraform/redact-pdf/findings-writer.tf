resource "google_service_account" "findings_writer" {
  account_id   = "findings-writer-sa${local.app_suffix}"
  display_name = "SA for Findings Writer function"
}

resource "google_project_iam_member" "findings_writer_bq_writer" {
  project = var.project_id
  role    = "roles/bigquery.dataEditor"
  member  = "serviceAccount:${google_service_account.findings_writer.email}"
}

resource "google_cloud_run_v2_service" "findings_writer" {
  name     = "findings-writer${local.app_suffix}"
  location = var.region
  ingress  = "INGRESS_TRAFFIC_INTERNAL_ONLY"

  template {
    containers {
      image = var.image_findings_writer
      env {
        name  = "BQ_DATASET"
        value = google_bigquery_dataset.redact_pdf.dataset_id
      }
      env {
        name  = "BQ_TABLE"
        value = google_bigquery_table.findings.table_id
      }
    }
    service_account = google_service_account.findings_writer.email
  }

  depends_on = [
    module.project_services,
  ]
}