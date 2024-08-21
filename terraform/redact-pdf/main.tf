terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.42.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "5.42.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

locals {
  app_suffix            = "-${var.suffix}"
  app_suffix_underscore = "_${var.suffix}"
}