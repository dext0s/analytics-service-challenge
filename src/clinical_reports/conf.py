import os
import re

# Debug environment variable
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
DB_SECRET_ARN = os.environ.get("DB_SECRET_ARN", "")
DB_RESOURCE_ARN = os.environ.get("DB_RESOURCE_ARN", "")
DB_NAME = os.environ.get("DB_NAME", "clinical")
DB_TABLE_NAME = os.environ.get("DB_TABLE_NAME", "clinical_reports")


def dump_config():
    return f"LOG_LEVEL: {LOG_LEVEL}\nDB_SECRET_ARN: {DB_SECRET_ARN}\nDB_RESOURCE_ARN: {DB_RESOURCE_ARN}\nDB_NAME: {DB_NAME}\nDB_TABLE_NAME: {DB_TABLE_NAME}"


UID_PATTERN = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
)
