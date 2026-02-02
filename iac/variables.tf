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
      methods = { 
        "POST" = { lambda_handler = "upload_reports_handler"}
        "GET" = { lambda_handler = "get_reports_handler"}
      }
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
    pandas = "../src/layer_pandera"
  }
}
variable "lambda-timeout" {
  type    = number
  default = 29
}
variable "lambda-python-version" {
  type    = string
  default = "3.13"
}
variable "lambda-arch" {
  type    = string
  default = "x86_64"
}
variable "aurora-postgresql-version" {
  type    = string
  default = "13.20"
}
variable "rds-table-name" {
  type    =  string
  default = "clinical_reports"
}
locals {
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
  lambda-layer-awswrangler-arn="arn:aws:lambda:${data.aws_region.current.name}:336392948345:layer:AWSSDKPandas-Python${replace(var.lambda-python-version,".","")}:6"
  layer-list = concat([local.lambda-layer-awswrangler-arn],[for layer in values(module.lambda_layer_local) : layer.lambda_layer_arn])
}