import logging
from .conf import LOG_LEVEL

logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)


STATUS_CODE = {
    "OK": 200,
    "INVALID_FORMAT": 415,
    "PARSING_ERROR": 500,
    "MISSING_FIELDS": 500,
    "CONSTRAINT_VIOLATION": 500,
    "DB_ERROR": 500,
    "UNKNOWN_ERROR": 500,
}

ERROR_MSG = {
    "INVALID_FORMAT": "The data format is incorrect. Please provide a valid CSV file.",
    "PARSING_ERROR": "There was an error processing the data. Please try again later.",
    "MISSING_FIELDS": "Required fields are missing from the data.",
    "CONSTRAINT_VIOLATION": "The data violates one or more constraints.",
    "UNKNOWN_ERROR": "An unknown error occurred.",
}


class HTTPException(Exception):
    def __init__(self, error_type: str, error_msg: str = None):
        self.error_type = error_type
        self.status_code = STATUS_CODE.get(error_type, 500)
        self.error_msg = (
            error_msg
            if error_msg is not None
            else ERROR_MSG.get(error_type, "An unknown error occurred.")
        )

    def to_dict(self):
        return {"statusCode": self.status_code, "body": self.error_msg}
