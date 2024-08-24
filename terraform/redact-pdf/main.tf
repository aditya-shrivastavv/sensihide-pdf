terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "=4.50.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "=4.50.0"
    }
  }
}

provider "google" {
  project     = var.project_id
  region      = var.region
  credentials = file(var.credentials_json)
}

locals {
  app_suffix            = "-${var.suffix}"
  app_suffix_underscore = "_${var.suffix}"
}