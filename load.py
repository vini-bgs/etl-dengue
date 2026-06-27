from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv
import os
from loguru import logger
from extract import csvs_for_df
from pathlib import Path

load_dotenv()


def get_engine():
    """
    Cria e retorna a conexão com o SQL Server
    """
    server = os.getenv("DB_SERVER")
    database = os.getenv("DB_DATABASE")

    conn_str = (
        f"mssql+pyodbc://@{server}/{database}"
        f"?driver=ODBC+Driver+17+for+SQL+Server"
        f"&trusted_connection=yes"
    )

    return create_engine(conn_str, fast_executemany=True)


def load_df_bronze(df: pd.DataFrame, engine) -> None:
    """
    Carrega o DataFrame na camada bronze do SQL Server
    """
    logger.info("⬆️ Iniciando carga na camada bronze...")

    df.to_sql(
        name="dengue_raw",
        con=engine,
        schema="bronze",
        if_exists="replace",
        index=False,
        chunksize=2000,
    )

    logger.info(f"✅ {len(df)} linhas carregadas em [bronze].[dengue_raw]")


if __name__ == "__main__":
    path = [Path("files/DENGBR20.csv")]
    df = csvs_for_df(path)
    engine = get_engine()
    load_df_bronze(df, engine)
