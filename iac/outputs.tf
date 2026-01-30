#Debug
# output "lambda-handlers-method-map" {
#   value = local.lambda-handlers-method-map
# }

# output "rest-api-paths" {
#   value = var.rest-api-paths
# }
output "api-endpoint-url" {
  value = aws_api_gateway_stage.api-gw-stage.invoke_url
}