module "project_services" {
  source  = "terraform-google-modules/project-factory/google//modules/project_services"
  version = "13.0.0"

  project_id = var.project_id

  activate_apis = [
    "run.googleapis.com",
    "bigquery.googleapis.com",
    "dlp.googleapis.com",
    "workflows.googleapis.com",
    "eventarc.googleapis.com",
    "pubsub.googleapis.com",
  ]

  disable_services_on_destroy = false
}