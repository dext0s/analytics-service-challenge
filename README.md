# analytics-service-challenge

## Definition
> Design and implement a simple cloud-based analytics service using AWS tools and services that can handle data ingestion, storage, and retrieval. 
>
>This challenge will test your skills in Python and AWS, as well as your ability to design a scalable and secure architecture.

More details on the reasoning [HERE](./docu/challenge_definition.md).

## Design summary

TO_DO define meaninguful examples 
TO_DO

More detail on the design [HERE](./docu/proposed_design.md)

## Backend local development

### Pre requisites
- Install Python 3.13
- Install and configure AWS CLI
- Bash shell
### Lambda code

To locally develop the python code for the lambda we use venv. To set it up run:
```bash
# Setup venv and install dependencies
pip3 install virtualenv
python3 -m venv venv
source venv/bin/activate
pip3 install -r src/requirements.txt
```

#### Testing
TO_DO

## Infrastructure code

Using Terraform to define the infrastructure. As per current requirements there is not a need to do multiples layers.

### Pre requisites
- Install and configure AWS CLI
- Install Terraform
- Bash shell
- Docker (due to Mac compativility issues)

We are using as backend provider S3 so the Terraform state is persisted.

Run the following script to setup an S3 bucket to store the state ({AccountID}-terraform-clinical-report).
Then initialize the terraform state usign the second script.
(Assuming you have al required permissions if not, [check this guide](https://developer.hashicorp.com/terraform/language/backend/s3))

```bash
# Set the region of preference:
export AWS_REGION="eu-central-1"
# Run once create terraform backend S3
bash setup/terraform_pre_req.sh
# Initialize terraform state
bash setup/terraform_setup.sh iac
# Mac workarround, pull build docker image:
docker pull public.ecr.aws/sam/build-python3.13:latest-x86_64
```

### Testing

To test terraform code we run a linting check, then a validation and finally a plan:
```bash
bash ./setup/terraform_test.sh iac
# To automatically fix linting issues run:
terraform fmt -recursive iac
```

## Setup

### Pre Requisites
    TO_DO
### Deploy
    TO_DO
### Test

You can use the following command to test:
```bash
# Push a report
base_url="https://YOUR_API_GATEWAY_ID.execute-api.us-east-1.amazonaws.com"
api_endpoint="${base_url}/v1/clinical-reports"
curl --request POST -H "Content-Type: text/csv" --data-binary "@./test/example.csv" "$api_endpoint"

# Get the list of pushed reports UIDs
curl --request GET "$api_endpoint"

# Get back the value of a certain record:
uri="35fcd1d9-359d-4b84-b62c-6999a5d03ea6"
curl --request GET "${api_endpoint}?uri=${uri}"
```
**Author: Xavier Torres**
