module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = "${var.app-name}-vpc"
  cidr = "10.0.0.0/16"

  azs              = [data.aws_availability_zones.available.names[0], data.aws_availability_zones.available.names[1]]
  database_subnets = ["10.0.21.0/24", "10.0.22.0/24"]
  private_subnets  = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets   = ["10.0.101.0/24", "10.0.102.0/24"]

  enable_nat_gateway = true

  tags = {
    Terraform = "true"
    Name      = "${var.app-name}-vpc"
  }
}