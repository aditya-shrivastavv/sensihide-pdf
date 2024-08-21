resource "google_data_loss_prevention_inspect_template" "dlp_pdf_template" {
  parent       = "projects/${var.project_id}/locations/global"
  description  = "Redact PDF Inspect Template"
  display_name = "redact_pdf_dlp_template"

  inspect_config {
    info_types {
      name = "PHONE_NUMBER"
    }
    info_types {
      name = "EMAIL_ADDRESS"
    }
    info_types {
      name = "PERSON_NAME"
    }
    info_types {
      name = "FIRST_NAME"
    }
    info_types {
      name = "LAST_NAME"
    }
  }

  depends_on = [module.project_services]
}