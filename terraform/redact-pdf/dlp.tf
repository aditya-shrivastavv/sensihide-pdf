resource "google_data_loss_prevention_inspect_template" "dlp_text_template" {
  parent       = "projects/${var.project_id}/locations/global"
  description  = "Redact Text Inspect Template"
  display_name = "redact_text_dlp_template"

  inspect_config {
    info_types {
      name = "PHONE_NUMBER"
    }
    info_types {
      name = "EMAIL_ADDRESS"
    }
    min_likelihood = "POSSIBLE"
    include_quote  = true
  }

  depends_on = [module.project_services]
}