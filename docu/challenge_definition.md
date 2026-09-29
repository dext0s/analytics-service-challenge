# Understanding the challenge

## Senior Backend Engineer - Challenge

### Objective:

The goal of this challenge is to assess your proficiency creating backends in Python on AWS. 

**Please include testing and documentation.**

### Challenge Overview:

Design and implement a simple cloud-based analytics service using AWS tools and services that can
handle data ingestion, storage, and retrieval.

This challenge will test your skills in Python and AWS, as
well as your ability to design a **scalable and secure architecture**.

**Please note that the candidate is expected to demonstrate a running code in the code walk through session.**

### Requirements:

Create a RESTful API using AWS Lambda and API Gateway that allows users to:

- Upload a CSV file containing drug discovery data (e.g., drug name, target, efficacy).

- Retrieve the uploaded data as a JSON response.

- Store the uploaded data in a database.

- Implement basic data validation, tests to ensure that the uploaded CSV has the correct format
and required fields.

- Ensure to document the code and your approach to the solution

---

## Questions

1. Formal definition of an "analytics service"?

From [AWS documentation](https://aws.amazon.com/what-is/data-analytics/):
> Data analytics converts raw data into actionable insights. It includes a range of tools, technologies, and processes used to find trends and solve problems using data. Data analytics can shape business processes, improve decision-making, and foster business growth.

2. Are the CSV files following the same schema?

As per the validation requirement we understand the **schema of the CSV files is fixed**.

3. Is CSV validation sync or async?

If the validation needs to be syncronous we are bounded to compute in the [maximum timeout the API GW allows by default which is 29 seconds](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-execution-service-limits-table.html).

As we are forced by the challenge definition to use Lambdas on the API GW, **I asume the response needs to be synchronous**.

4. Which is the expected size of this CSV files?

Depending on the max size of the CSV file we need to support it will define how the system ingest the data and how the user retrieves it.

[AWS REST API GW quota is 10MB for the payload](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-execution-service-limits-table.html).

But if we are forced to ingest using a Lambda [invocation payload is limited to 6MB](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html).

In case we need to support bigger files the systme needs to change the upload method and implement pagination for data retrieval.


5. From Q1, what are the steps that the data take:
    
    1. Data collection: [Options reference](https://aws.amazon.com/blogs/compute/patterns-for-building-an-api-to-upload-files-to-amazon-s3/)
        - API GW as Direct proxy to S3 (Max file size 10MB).
        - **API GW + Lambda then to S3 (Max file size 6MB).**
        - Presigned URL (Max file size  5GB).
    2. Data storage: 
        - Raw file: **S3**
        - "Processed" (we are not doing any transform to the data): **RDS**  
    3. Data processing: **Lambda**
    4. Data cleansing (No actively correcting, only validating): **Lambda**
    5. Data analysis (Not relevant for the challenge): for example we could use AWS Glue Catalog + Athena or use [Athena's Federated Query](https://aws.amazon.com/es/blogs/big-data/query-any-data-source-with-amazon-athenas-new-federated-query/) to fetch directly from RDS

6. Which type of collection (ingestion) is best practise for this example? Batch processing or streaming?

This higly depend on factors that are not defined explicitly on the challenge like the max size of data we need to handle per transaction or the overall scale required.

As we have a predefined technology solutions if bonded to its restricions.

As the Max size of the payload is relatively small and we will be able to respond in a Real Time fashion (less than 30s) **Stream processing seems the better fit.**

7. ETL vs ELT: which one to choose in this case?

System receive, validate and store. **So ETL is the best match.**

8. Which type of DB make sense for this example?

For this approach, as the Schema is fixed as per Q2, any SQL DB should do the trick.**I'll use Postgres.**

9. Summary of REST fundamentals RESTful best practices:

Answer in [THIS](./REST_refresh.md) document.

10. Can all users access all the uploaded data, or there must be any kind of management?

Data Governance wise there should be a management on who can access the data (for instance using user groups). But to not overcomplicate the challenge we will assume all users can access all data.

## What I know/ What I learned

### I know

1. Most of the AWS services and the relationship between them.
2. How to define them using Terraform.
3. How to structure and design the Python code to support the features.
4. How to setup a secure and scalable infrastructure.

### What I learned

1. What is a Data Analytics system.
2. Best practices to implement a Data Analytics system.
3. Best practices to implement a RESTful API.
4. Details on Lambda layer building.

## Documentation checked

1. [AWS Whitepaper "Storage Best Practices for Data and Analytics Applications"](https://docs.aws.amazon.com/whitepapers/latest/building-data-lakes/building-data-lake-aws.html)
2. [Patterns for building an API to upload files to Amazon S3](https://aws.amazon.com/blogs/compute/patterns-for-building-an-api-to-upload-files-to-amazon-s3/)
3. [Glue connecting data](https://docs.aws.amazon.com/glue/latest/dg/glue-connections.html)
4. [Using the CSV format in AWS Glue](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-format-csv-home.html)
5. [Batch vs. streaming data processing](https://docs.databricks.com/aws/en/data-engineering/batch-vs-streaming)
6. [ETL vs ELT](https://aws.amazon.com/compare/the-difference-between-etl-and-elt/)
7. [File upload best practices](https://www.speakeasy.com/api-design/file-uploads)
8. [OWASP Secure file upload](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html)
