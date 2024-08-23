variable "region" {
  description = "Google cloud region"
  type        = string
  default     = "us-central1"
}

variable "wf_region" {
  type        = string
  description = "Cloud Workflows Region (choose a supported region: https://cloud.google.com/workflows/docs/locations)"
  default     = "us-central1"
}