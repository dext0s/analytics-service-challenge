resource "aws_api_gateway_rest_api" "api-gw" {
  name        = "${var.app-name}-api-gw"
  description = "API Gateway for ${var.app-name} application"
  body = jsonencode({
    openapi = "3.0.1"
    info = {
      title       = "${var.app-name} API"
      description = "API Gateway for ${var.app-name} application"
      version     = "1.0.0"
    }
    paths = {
      for api_path, v in var.rest-api-paths : api_path => {
        for method, conf in v.methods : lower(method) => {
          x-amazon-apigateway-integration = {
            uri        = module.lambdas[conf.lambda_handler].lambda_function_invoke_arn
            httpMethod = method
            type       = "aws_proxy"
          }
        }
      }
    }

  })
  endpoint_configuration {
    types = ["REGIONAL"]
  }

}


resource "aws_api_gateway_deployment" "deploy-api" {
  rest_api_id = aws_api_gateway_rest_api.api-gw.id

  triggers = {
    redeployment = sha1(jsonencode(aws_api_gateway_rest_api.api-gw.body))
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "api-gw-stage" {
  deployment_id = aws_api_gateway_deployment.deploy-api.id
  rest_api_id   = aws_api_gateway_rest_api.api-gw.id
  stage_name    = var.api-gw-stage-name
}