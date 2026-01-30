import boto3
from .clinical_report import ClinicalReport
from .conf import DB_SECRET_ARN, DB_RESOURCE_ARN, DB_NAME
from .logs import logger, HTTPException

# with wr.data_api.rds.connect(
#     resource_arn=DB_RESOURCE_ARN, secret_arn=DB_SECRET_ARN, database=DB_NAME
# ) as db_session:

def db_store_clinical_report(cr: ClinicalReport):
    try:
        # wr.data_api.rds.to_sql(
        #     cr.t_df,
        #     con=db_session,
        #     table="clinical_reports",
        #     if_exists="append",
        #     index=False,
        # )
        pass  # Placeholder for actual database operation
    except Exception as e:
        logger.error(f"Error connecting to database: {str(e)}")
        raise HTTPException("DB_ERROR", f"{str(e)}")
    pass