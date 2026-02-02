import argparse
import uuid
import time
from clinical_reports.logs import logger, HTTPException
from clinical_reports.clinical_report import ClinicalReport, check_uid
from clinical_reports.db import (
    db_store_clinical_report,
    db_get_clinical_report_list,
    db_get_clinical_report,
)


def upload_reports_handler(event, context):
    try:
        raw_data = event["body"]
        request_id = event["requestContext"]["requestId"]
        epoch = event["requestContext"]["requestTimeEpoch"]
        report = ClinicalReport.from_csv(raw_data, uid=request_id, epoch=epoch)
        db_store_clinical_report(report)
    except HTTPException as e:
        logger.error(f"Error processing report: {e.error_msg}")
        return e.to_dict()
    except Exception as e:
        logger.error(f"UNKNOWN_ERROR: {str(e)}")
        return HTTPException("UNKNOWN_ERROR").to_dict()
    return {"statusCode": 200, "body": report.get_json(with_metadata=True)}


def get_reports_handler(event, context):
    try:
        query_params = event.get("queryStringParameters", None)
        if query_params is None:
            list_of_reports = db_get_clinical_report_list()
            return {
                "statusCode": 200,
                "body": list_of_reports.to_json(orient="records"),
            }
        else:
            uid = query_params.get("uid", None)
            if uid is None:
                raise HTTPException(
                    "UNKNOWN_QUERY_PARAMS",
                    "Currently only support 'uid' as query parameter.",
                )
            check_uid(uid)
            report = db_get_clinical_report(uid=uid)
            return {"statusCode": 200, "body": report.get_json()}
    except HTTPException as e:
        logger.error(f"Error fetching report: {e.error_msg}")
        return e.to_dict()
    except Exception as e:
        logger.error(f"UNKNOWN_ERROR: {str(e)}")
        return HTTPException("UNKNOWN_ERROR").to_dict()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--handler",
        type=str,
        choices=["upload_reports_handler", "get_reports_handler"],
        required=True,
        help="Specify which handler to test.",
    )
    parser.add_argument(
        "--csv_file", type=str, help="Path to CSV file for upload_reports_handler."
    )
    parser.add_argument("--uid", type=str, help="UID for get_reports_handler.")
    args = parser.parse_args()
    mock_event = dict(
        {
            "body": "",
            "queryStringParameters": {"uid": args.uid} if args.uid else None,
            "requestContext": {
                "requestId": "35fcd1d9-359d-4b84-b62c-6999a5d03ea6",  # Force a UUID for testing
                "requestTimeEpoch": int(time.time() * 1000),
            },
        }
    )
    if args.handler == "upload_reports_handler" and args.csv_file:
        with open(args.csv_file, "r") as f:
            mock_event["body"] = f.read()

    mock_context = dict({})
    if args.handler == "upload_reports_handler":
        response = upload_reports_handler(mock_event, mock_context)
    else:
        response = get_reports_handler(mock_event, mock_context)
    print(response)
