from extract import csvs_for_df
from pathlib import Path
import pandas as pd


def profile_columns(df: pd.DataFrame) -> dict:
    """
    Recebe o DataFrame e infere qual o tipo de cada
    coluna para ser utilizado no Schema da tabela
    """
    schema = dict()
    df = df.head(1000)

    for col in df.columns:
        sample = df[col].dropna()

        if len(sample) == 0:
            schema[col] = "str"
            continue

        converted = pd.to_datetime(sample, errors="coerce", format="%Y-%m-%d")
        if converted.notna().sum() / len(sample) > 0.8:
            schema[col] = "date"
            continue

        converted = pd.to_numeric(sample, errors="coerce")
        if converted.notna().sum() / len(sample) > 0.8:
            if (converted.dropna() % 1 == 0).all():
                schema[col] = "int"
            else:
                schema[col] = "float"
            continue

        schema[col] = "str"

    return schema


if __name__ == "__main__":
    path = [Path("files/DENGBR20.csv")]
    df = csvs_for_df(path)
    schema = profile_columns(df)
    print(schema)
