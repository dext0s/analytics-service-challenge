data "aws_region" "current" {}

data "aws_availability_zones" "available" {}

data "aws_caller_identity" "current" {}

variable "app-name" {
  type    = string
  default = "clinical-reports"
}
variable "rest-api-paths" {
  description = "Map that configures API Gateway resources and their HTTP methods and Lambda handlers"
  type = map(object({
    methods = map(object({
      lambda_handler = string
    }))
  }))
  default = {
    "/clinical-reports" = {
      methods = { "POST" = {
        lambda_handler = "upload_reports_handler"
      } }
    }
  }
}
variable "api-gw-stage-name" {
  type    = string
  default = "v1"
}
variable "lambda-handler-file" {
  type    = string
  default = "lambda_handlers"
}
variable "lambda-source-path" {
  type    = string
  default = "../src"
}
variable "lambda-layer-paths" {
  type    = map(string)
  default = {
    sqlAlchemy = "../src/layer_SQLAlchemy"
    pandas = "../src/layer_pandas"
  }
}
variable "lambda-timeout" {
  type    = number
  default = 29
}
variable "python-runtime" {
  type    = string
  default = "python3.13"
}
variable "aurora-postgresql-version" {
  type    = string
  default = "13.20"
}
locals {
  #lambda-handlers-method-map = {upload_reports_handler={path = "/clinical-reports", http_method = "POST", lambda_handler = "upload_reports_handler"}}
  lambda-handlers-method-map = {
    for item in flatten([
      for path, cfg in var.rest-api-paths : [
        for http_method, m in cfg.methods : {
          handler     = m.lambda_handler
          path        = path
          http_method = http_method
        }
      ]
      ]) : item.handler => {
      path           = item.path
      http_method    = item.http_method
      lambda_handler = item.handler
    }
  }
}