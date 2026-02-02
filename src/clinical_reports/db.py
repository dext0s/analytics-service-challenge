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
        except Exception as e:
            logger.error(f"Error connecting to database: {str(e)}")
            raise HTTPException("DB_ERROR", f"{str(e)}")
        
    def db_get_clinical_report_list():
        try:
            df = wr.data_api.rds.read_sql_query(
                sql=f'SELECT DISTINCT "UID", "Epoch" FROM {DB_TABLE_NAME} ORDER BY "Epoch" DESC;',
                con=db_session,
                database=DB_NAME,
            )
            return df
        except Exception as e:
            logger.error(f"Error connecting to database: {str(e)}")
            raise HTTPException("DB_ERROR", f"{str(e)}")

    def db_get_clinical_report(uid: str) -> ClinicalReport:
        try:
            df = wr.data_api.rds.read_sql_query(
                sql=f'SELECT * FROM {DB_TABLE_NAME} WHERE "UID" = \'{uid}\'',
                con=db_session,
                database=DB_NAME,
            )
            if df.empty: raise HTTPException("REPORT_NOT_FOUND", f"No report found with UID: {uid}")
            return ClinicalReport.from_transform_df(df)
        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"Error connecting to database: {str(e)}")
            raise HTTPException("DB_ERROR", f"{str(e)}")