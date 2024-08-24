resource "google_service_account" "pdf_redactor" {
  account_id   = "pdf-redactor-sa${local.app_suffix}"
  display_name = "SA for Redact PDF"
}

resource "google_project_iam_member" "pdf_redactor_storage_user" {
  project = var.project_id
  role    = "roles/storage.admin"
  member  = "serviceAccount:${google_service_account.pdf_redactor.email}"
}

resource "google_cloud_run_v2_service" "pdf_redactor" {
  name     = "pdf-redactor${local.app_suffix}"
  location = var.region
  ingress  = "INGRESS_TRAFFIC_INTERNAL_ONLY"

  template {
    containers {
      image = var.image_pdf_redactor
    }
    service_account = google_service_account.pdf_redactor.email
  }

  depends_on = [
    module.project_services,
  ]
}