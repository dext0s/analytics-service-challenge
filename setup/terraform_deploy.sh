#!/bin/bash
AWS_DEFAULT_REGION="eu-central-1"

if [ -z "${AWS_REGION}" ]; then
    echo "Environment variable AWS_REGION not set. Defaulting to ${AWS_DEFAULT_REGION}."
    export AWS_REGION="$AWS_DEFAULT_REGION"
fi
echo "Module Path: $1"
[ $# -ne 1 ] && echo "Usage: $0 <module path>" 1>&2 && exit 1
base_dir=$(pwd)
cd "$1"

terraform apply -auto-approve
# Setup source file with terraform outputs
echo "" > ${base_dir}/terraform_outputs_source.sh
for var in AWS_REGION DB_NAME DB_RESOURCE_ARN DB_SECRET_ARN DB_TABLE_NAME api_endpoint_url; do
    value=$(terraform output -raw "$var")
    echo "export ${var}=\"${value}\"" >> ${base_dir}/terraform_outputs_source.sh
done