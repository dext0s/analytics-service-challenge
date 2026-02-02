output "api_endpoint_url" {
  # format like https://z4675bid1j.execute-api.eu-west-2.amazonaws.com/prod
  value = aws_api_gateway_stage.api-gw-stage.invoke_url
}
output "DB_SECRET_ARN" {
  value = aws_rds_cluster.rds-cluster.master_user_secret[0].secret_arn
}
output "DB_RESOURCE_ARN" {
  value =  aws_rds_cluster.rds-cluster.arn
}
output "DB_NAME" {
   value = aws_rds_cluster.rds-cluster.database_name
}
output "DB_TABLE_NAME" {
  value = var.rds-table-name
}
output "AWS_REGION" {
  value = data.aws_region.current.region
}