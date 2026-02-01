module "lambdas" {
  source        = "terraform-aws-modules/lambda/aws"
  for_each      = local.lambda-handlers-method-map
  function_name = "${var.app-name}-${each.value.lambda_handler}"
  handler       = "${var.lambda-handler-file}.${each.value.lambda_handler}"
  runtime       = "python${var.lambda-python-version}"
  memory_size = 1024
  timeout       = var.lambda-timeout
  layers        = local.layer-list
  architectures = [var.lambda-arch]
  publish       = true
  # Build
  source_path   = [{path = var.lambda-source-path, pip_requirements = false , patterns = ["!layer_.*/*"]}]
  docker_build_root   = "${var.lambda-source-path}"
  build_in_docker     = true
  docker_image        = "public.ecr.aws/sam/build-python${var.lambda-python-version}:latest-x86_64"
  # Config
  environment_variables = {
    LOG_LEVEL       = "DEBUG"
    DB_SECRET_ARN   = aws_rds_cluster.rds-cluster.master_user_secret[0].secret_arn
    DB_RESOURCE_ARN = aws_rds_cluster.rds-cluster.arn
    DB_NAME         = aws_rds_cluster.rds-cluster.database_name
    DB_TABLE_NAME      = var.rds-table-name
  }
  attach_policy = true
  policy = aws_iam_policy.allow-rds-data-api-usage.arn
}

module "lambda_layer_local" {
  source = "terraform-aws-modules/lambda/aws"
  for_each = var.lambda-layer-paths
  create_layer = true

  layer_name          = "${var.app-name}-${each.key}-deps"
  description         = "${var.app-name} dependencies layer"
  compatible_runtimes = ["python${var.lambda-python-version}"]
  runtime = "python${var.lambda-python-version}"
  source_path         = [{path = "${path.root}/${each.value}/", pip_requirements = true ,prefix_in_zip    = "python"}]
  docker_build_root   = "${path.root}/${each.value}"
  build_in_docker     = true
  docker_image        = "public.ecr.aws/sam/build-python${var.lambda-python-version}:latest-x86_64"
}

# Manually seting allow triggers as there is a cycle issue when using this lamdba module together with API Gateway defined with OpenAPI
resource "aws_lambda_permission" "lambda-invoke-permission" {
  for_each      = local.lambda-handlers-method-map
  statement_id  = "AllowApiGatewayInvoke_${each.value.lambda_handler}"
  action        = "lambda:InvokeFunction"
  function_name = "${var.app-name}-${each.value.lambda_handler}"
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.api-gw.execution_arn}/${var.api-gw-stage-name}/${each.value.http_method}${each.value.path}"
}