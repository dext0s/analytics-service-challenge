resource "aws_rds_cluster" "rds-cluster" {
  cluster_identifier                  = "${var.app-name}-rds-cluster"
  engine                              = "aurora-postgresql"
  engine_mode                         = "provisioned"
  db_subnet_group_name                = module.vpc.database_subnet_group_name
  engine_version                      = var.aurora-postgresql-version
  iam_database_authentication_enabled = true
  enable_http_endpoint                 = true
  database_name                       = "clinical"
  manage_master_user_password         = true
  master_username                     = "clinical_admin"
  skip_final_snapshot                 = true 
  serverlessv2_scaling_configuration {
    max_capacity             = 1.0
    min_capacity             = 0.0
    seconds_until_auto_pause = 3600
  }
}

resource "aws_rds_cluster_instance" "rds-cluster-instance" {
  cluster_identifier = aws_rds_cluster.rds-cluster.id
  instance_class     = "db.serverless"
  engine             = aws_rds_cluster.rds-cluster.engine
  engine_version     = aws_rds_cluster.rds-cluster.engine_version
}

resource "aws_iam_policy" "allow-rds-data-api-usage" {
  name        = "allow-rds-data-api-usage"
  path        = "/"
  description = "${var.app-name} policy to allow RDS Data API usage"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "secretsmanager:GetSecretValue",
        ]
        Effect   = "Allow"
        Resource = "${aws_rds_cluster.rds-cluster.master_user_secret[0].secret_arn}"
      },
      {
        Action = [
          "rds-data:ExecuteStatement",
          "rds-data:BatchExecuteStatement",
          "rds-data:BeginTransaction",
          "rds-data:CommitTransaction",
          "rds-data:RollbackTransaction",
        ]
        Effect   = "Allow"
        Resource = "${aws_rds_cluster.rds-cluster.arn}"
      },
    ]
  })
}