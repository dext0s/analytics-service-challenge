import pandas as pd
import pandera.pandas as pa
import argparse

class ClinicalReportSchema(pa.DataFrameModel):
    SubstanceID: pa.typing.Series[str]
    DrugName: pa.typing.Series[str] = pa.Field(nullable=True)
    Target: pa.typing.Series[str] = pa.Field(nullable=True)
    Efficacy: pa.typing.Series[float]
    Toxicity: pa.typing.Series[float] = pa.Field(nullable=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n",
        type=int,
        required=True,
        help="Specify ammount of rows to generate.",
    )
    argargs = parser.parse_args()
    df = ClinicalReportSchema.empty()

    # Generate a random set of examples
    rows=[]
    for i in range(argargs.n):
        rows.append({
            "SubstanceID": f"S{i:05d}",
            "DrugName": None if i % 5 == 0 else f"Drug_{i}",
            "Target": None if i % 7 == 0 else f"Target_{i%3}",
            "Efficacy": float(i) * 1.5,
            "Toxicity": None if i % 4 == 0 else float(i) * 0.5,
        })
    
    df = pd.DataFrame(rows)
    df.to_csv(f"generated_clinical_reports_{argargs.n}.csv", index=False)