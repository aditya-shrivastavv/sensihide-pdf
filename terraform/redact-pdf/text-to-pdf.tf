resource "google_service_account" "pdf_to_text" {
  account_id   = "pdf-to-text-sa${local.app_suffix}"
  display_name = "SA for text extraction from PDFs"
}

resource "google_project_iam_member" "pdf_to_text_storage_user" {
  project = var.project_id
  role    = "roles/storage.admin"
  member  = "serviceAccount:${google_service_account.pdf_to_text.email}"
}

resource "google_cloud_run_v2_service" "pdf_to_text" {
  name     = "pdf-to-text${local.app_suffix}"
  location = var.region
  ingress = "INGRESS_TRAFFIC_INTERNAL_ONLY"

  template {
    containers {
      image = "Image"
    }
    service_account = google_service_account.pdf_to_text.email
  }

  depends_on = [
    module.project_services,
  ]
}