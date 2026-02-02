import pandas as pd
import pandera.pandas as pa
import uuid
import time
import json
from io import StringIO
from .logs import HTTPException


class ClinicalReportSchema(pa.DataFrameModel):
    SubstanceID: pa.typing.Series[str]
    DrugName: pa.typing.Series[str] = pa.Field(nullable=True)
    Target: pa.typing.Series[str] = pa.Field(nullable=True)
    Efficacy: pa.typing.Series[float]
    Toxicity: pa.typing.Series[float] = pa.Field(nullable=True)


class ClinicalReportSchemaPersistence(pa.DataFrameModel):
    UID: pa.typing.Series[str]
    Epoch: pa.typing.Series[int]
    SubstanceID: pa.typing.Series[str]
    DrugName: pa.typing.Series[str] = pa.Field(nullable=True)
    Target: pa.typing.Series[str] = pa.Field(nullable=True)
    Efficacy: pa.typing.Series[float]
    Toxicity: pa.typing.Series[float] = pa.Field(nullable=True)


class ClinicalReport:
    def __init__(self, df: pd.DataFrame, t_df: pd.DataFrame = None, uid: str = None, epoch: int = None):
        self.df = df
        self.t_df = t_df
        self.uid = uid if uid is not None else str(uuid.uuid4())
        self.epoch = epoch if epoch is not None else int(time.time() * 1000)

    def get_df(self):
        return self.df

    def get_transform_df(self):
        try:
            if self.t_df is None:
                self.t_df = self.df.copy()
                self.t_df.insert(0, "UID", self.uid)
                self.t_df.insert(1, "Epoch", self.epoch)
        except Exception as e:
            raise HTTPException("TRANSFORMATION_ERROR", str(e))
        return self.t_df

    def get_json(self, with_metadata: bool = False):
        if with_metadata:
            md = json.dumps({"UID": self.uid, "Epoch": self.epoch})
            data = self.df.to_json(orient="records")
            return f"{md},{data}"
        return self.df.to_json(orient="records")

    @classmethod
    def from_csv(cls, raw_csv, uid: str = None, epoch: int = None):
        try:
            df = pd.read_csv(StringIO(raw_csv), on_bad_lines="error")
            df = ClinicalReportSchema.validate(df)
        except UnicodeError as e:
            raise HTTPException("INVALID_FORMAT")
        except Exception as e:
            raise HTTPException("PARSING_ERROR", str(e))
        except pa.errors.SchemaError as e:
            raise HTTPException("CONSTRAINT_VIOLATION", str(e))
        return ClinicalReport(df, uid=uid, epoch=epoch)

    @classmethod
    def from_transform_df(cls, t_df: pd.DataFrame):
        try:
            t_df = ClinicalReportSchemaPersistence.validate(t_df)
            uid = t_df["UID"].iloc[0]
            epoch = t_df["Epoch"].iloc[0]
            df = t_df.copy().drop(columns=["UID", "Epoch"])
        except pa.errors.SchemaError as e:
            raise HTTPException("CONSTRAINT_VIOLATION", str(e))
        return ClinicalReport(df, t_df=t_df, uid=uid, epoch=epoch)