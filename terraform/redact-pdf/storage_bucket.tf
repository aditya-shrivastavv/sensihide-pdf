resource "google_storage_bucket" "pdf_input_bucket" {
  name                        = "pdf-input-bucket${local.app_suffix}"
  location                    = var.region
  uniform_bucket_level_access = true
  force_destroy               = true
}

resource "google_storage_bucket" "buffer_bucket" {
  name                        = "buffer-bucket${local.app_suffix}"
  location                    = var.region
  uniform_bucket_level_access = true
  force_destroy               = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "Delete"
    }
  }

}

resource "google_storage_bucket" "pdf_output_bucket" {
  name                        = "pdf-output-bucket${local.app_suffix}"
  location                    = var.region
  uniform_bucket_level_access = true
  force_destroy               = true
}