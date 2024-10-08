variable "project_id" {
  description = "Project ID"
  type        = string
}

variable "region" {
  description = "Google cloud region"
  type        = string
}

variable "suffix" {
  description = "Suffix to append to resources (3 to 6 chars)"
  validation {
    condition     = length(var.suffix) > 3 && length(var.suffix) < 6
    error_message = "Suffix must be between 3 and 6 characters"
  }
}

variable "image_pdf_to_text" {
  default     = "adityadocs/sensihidepdf-pdf-to-text:latest"
  description = "Image for the PDF to text service"
  type        = string
}

variable "image_dlp_runner" {
  default     = "adityadocs/sensihidepdf-dlp-runner:latest"
  description = "Image for the DLP runner service"
  type        = string
}

variable "image_findings_writer" {
  default     = "adityadocs/sensihidepdf-findings-writer:latest"
  description = "Image for the findings writer service"
  type        = string
}

variable "image_pdf_redactor" {
  default     = "adityadocs/sensihidepdf-redactor:latest"
  description = "Image for the PDF redactor service"
  type        = string
}

variable "credentials_json" {
  description = "Path to the credentials JSON file"
  type        = string
}