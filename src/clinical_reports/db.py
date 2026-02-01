import boto3
import awswrangler as wr
from .clinical_report import ClinicalReport
from .conf import DB_SECRET_ARN, DB_RESOURCE_ARN, DB_NAME, DB_TABLE_NAME
from .logs import logger, HTTPException

with wr.data_api.rds.connect(
    resource_arn=DB_RESOURCE_ARN, secret_arn=DB_SECRET_ARN, database=DB_NAME
) as db_session:

    def db_store_clinical_report(cr: ClinicalReport):
        try:
            wr.data_api.rds.to_sql(
                df=cr.get_transform_df(),
                con=db_session,
                database=DB_NAME,
                table=DB_TABLE_NAME,
                use_column_names=True,
                sql_mode="ansi"
            )
        except wr.exceptions.DatabaseErrorException as e:
            logger.error(f"Error connecting to database: {str(e)}")
            raise HTTPException("DB_ERROR", f"{str(e)}")
        except Exception as e:
            logger.error(f"Unknown error during DB operation: {str(e)}")
            raise HTTPException("UNKNOWN_ERROR", f"{str(e)}")