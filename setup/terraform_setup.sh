#!/bin/bash
AWS_DEFAULT_REGION="eu-central-1"

echo "Module Path: $1"
[ $# -ne 1 ] && echo "Usage: $0 <module path>" 1>&2 && exit 1
cd "$1"

if [ -z "${AWS_REGION}" ]; then
    echo "Environment variable AWS_REGION not set. Defaulting to ${AWS_DEFAULT_REGION}."
    export AWS_REGION="$AWS_DEFAULT_REGION"
fi
rm -rf .terraform
# Get you AWS account ID
account_id=$(aws sts get-caller-identity --query Account --output text)
# Bucket name
bucket_name="${account_id}-terraform-clinical-report"

echo "Initializing terraform"
terraform init -backend-config="bucket=${bucket_name}"