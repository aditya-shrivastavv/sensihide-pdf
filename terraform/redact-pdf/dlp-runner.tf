resource "google_service_account" "dlp_runner" {
  project      = var.project_id
  account_id   = "dlp-runner-sa${local.app_suffix}"
  display_name = "SA for DLP Runner function"
}

resource "google_project_iam_member" "dlp_runner_dlp_user" {
  project = var.project_id
  role    = "roles/dlp.user"
  member  = "serviceAccount:${google_service_account.dlp_runner.email}"
}

resource "google_project_iam_member" "dlp_runner_dlp_template_reader" {
  project = var.project_id
  role    = "roles/dlp.inspectTemplatesReader"
  member  = "serviceAccount:${google_service_account.dlp_runner.email}"
}

resource "google_cloud_run_v2_service" "dlp_runner" {
  name     = "dlp-runner${local.app_suffix}"
  location = var.region
  ingress  = "INGRESS_TRAFFIC_INTERNAL_ONLY"

  template {
    containers {
      image = "Image"
    }
    service_account = google_service_account.dlp_runner.email
  }

  depends_on = [module.project_services]
}