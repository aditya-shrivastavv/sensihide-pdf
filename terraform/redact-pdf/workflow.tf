resource "google_service_account" "workflow" {
  account_id   = "redact-pdf-workflow-sa${local.app_suffix}"
  display_name = "SA for Redact PDF Workflow"
}

resource "google_project_iam_member" "workflow_cloudrun_invoker" {
  project = var.project_id
  role    = "roles/run.invoker"
  member  = "serviceAccount:${google_service_account.workflow.email}"
}

resource "google_project_iam_member" "workflow_log_writer" {
  project = var.project_id
  role    = "roles/logging.logWriter"
  member  = "serviceAccount:${google_service_account.workflow.email}"
}

resource "google_project_iam_member" "workflow_event_receiver" {
  project = var.project_id
  role    = "roles/eventarc.eventReceiver"
  member  = "serviceAccount:${google_service_account.workflow.email}"
}

resource "google_workflows_workflow" "redact_pdf" {
  name            = "redact-pdf-workflow${local.app_suffix}"
  region          = var.region
  description     = "Workflow that redacts sensitive information from a single PDF file"
  service_account = google_service_account.workflow.id
  source_contents = templatefile(
    "${path.module}/templates/workflow.yaml",
    {
      output_bucket       = google_storage_bucket.output_bucket.name
      pdf_to_text_url     = google_cloud_run_v2_service.pdf_to_text.uri
      dlp_runner_url      = google_cloud_run_v2_service.dlp_runner.uri
      dlp_template        = google_data_loss_prevention_inspect_template.dlp_text_template.id
      findings_writer_url = google_cloud_run_v2_service.findings_writer.uri
      redact_pdf_url = google_cloud_run_v2_service.pdf_redactor.uri
    }
  )

  depends_on = [module.project_services]
}