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
  default = "adityadocs/sensihidepdf-pdf-to-text:latest"
  description = "Image for the PDF to text service"
  type        = string
}