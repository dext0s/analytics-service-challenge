import os

# Debug environment variable
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
DB_SECRET_ARN = os.environ.get("DB_SECRET_ARN", "")
DB_RESOURCE_ARN = os.environ.get("DB_RESOURCE_ARN", "")
DB_NAME = os.environ.get("DB_NAME", "clinical_reports_db")
