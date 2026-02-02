terraform {
  backend "s3" {
    key     = "clinical_report.tfstate"
    region  = "eu-central-1"
    encrypt = true
  }
}