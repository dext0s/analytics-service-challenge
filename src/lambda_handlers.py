from clinical_reports.logs import logger, HTTPException
from clinical_reports.clinical_report import ClinicalReport
from clinical_reports.db import db_store_clinical_report, db_get_clinical_report_list, db_get_clinical_report


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
        if not query_params == None:
            uid = query_params.get("uid", None)
            # ensure UID is UID format
            if uid is None:
                raise HTTPException("UNKNOWN_QUERY_PARAMS", "Currently only support 'uid' as query parameter.")
            report = db_get_clinical_report(uid=uid)
            return {"statusCode": 200, "body": report.get_json()}
        else:
            list_of_reports = db_get_clinical_report_list()
            return {"statusCode": 200, "body": list_of_reports.to_json(orient="records")}
    except HTTPException as e:
        logger.error(f"Error fetching report: {e.error_msg}")
        return e.to_dict()
    except Exception as e:
        logger.error(f"UNKNOWN_ERROR: {str(e)}")
        return HTTPException("UNKNOWN_ERROR").to_dict()

if __name__ == "__main__":
    mock_event = dict(
        {
            "body": "SubstanceID,DrugName,Target,Efficacy,Toxicity\nSID-12345,Test1,,0.1,0.3\nSID-67890,Test2,heart,0.99,0.3",
            "requestContext": {
                "requestId": "35fcd1d9-359d-4b84-b62c-6999a5d03ea6",
                "requestTimeEpoch": 1769475269867,
            },
        }
    )
    # mock_event = dict({'body' : ',,,,ewhrwprhwerhiaiosdh', 'requestContext' : { 'requestId': '35fcd1d9-359d-4b84-b62c-6999a5d03ea6', 'requestTimeEpoch': 1769475269867 }})
    # mock_event = dict({'body' : 'SubstanceID,DrugName,Target,Efficacy,Toxicity\n,,,,ewhrwprhwerhiaiosdh', 'requestContext' : { 'requestId': '35fcd1d9-359d-4b84-b62c-6999a5d03ea6', 'requestTimeEpoch': 1769475269867 }})

    mock_context = dict({})
    response = upload_reports_handler(mock_event, mock_context)
    print(response)
