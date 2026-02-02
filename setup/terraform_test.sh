#!/bin/bash
set -e
echo "Module Path: $1"
[ $# -ne 1 ] && echo "Usage: $0 <module path>" 1>&2 && exit 1
cd "$1"

terraform fmt -recursive
terraform validate
terraform plan