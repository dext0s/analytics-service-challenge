#!/bin/bash
AWS_DEFAULT_REGION="eu-central-1"

if [ -z "${AWS_REGION}" ]; then
    echo "Environment variable AWS_REGION not set. Defaulting to ${AWS_DEFAULT_REGION}."
    export AWS_REGION="$AWS_DEFAULT_REGION"
fi
# Get you AWS account ID
account_id=$(aws sts get-caller-identity --query Account --output text)
# Creates a S3 bucket for Terraform state storage
aws s3api create-bucket --bucket "${account_id}-terraform-clinical-report" --region "${AWS_REGION}" --create-bucket-configuration LocationConstraint=$AWS_REGION