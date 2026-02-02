#!/bin/bash
AWS_DEFAULT_REGION="eu-central-1"

if [ -z "${AWS_REGION}" ]; then
    echo "Environment variable AWS_REGION not set. Defaulting to ${AWS_DEFAULT_REGION}."
    export AWS_REGION="$AWS_DEFAULT_REGION"
fi
echo "Module Path: $1"
[ $# -ne 1 ] && echo "Usage: $0 <module path>" 1>&2 && exit 1
cd "$1"

terraform apply