import pandas as pd


from tqdm import tqdm
from pathlib import Path
from loguru import logger


def list_files(pasta: Path) -> list:
    """
    Recebe uma pasta e retorna uma lista com o nome
     de todos os arquivos .csv daquela pasta
    """
    if not pasta.exists():
        logger.error(f"🛑 Arquivo não encontrado: {pasta}")
        raise FileNotFoundError(f"🛑 Arquivo não encontrado: {pasta}")

    lista_arquivos = list(pasta.glob("*.csv"))

    qtde_arquivos = len(lista_arquivos)
    logger.info(
        f"📄 Foram encontrados {qtde_arquivos} arquivos dentro da pasta {pasta}"
    )

    return lista_arquivos


def csvs_for_df(arquivos: list) -> pd.DataFrame:
    """
    Lê os arquivos .csv de uma pasta e armazena em uma variável
    """
    lista_df = list()
    # count = 1
    # qtde_arquivos = len(arquivos)
    for arquivo in tqdm(arquivos):
        df_temp = pd.read_csv(arquivo, dtype=str, encoding="utf-8")
        df_temp["origem"] = arquivo.name
        lista_df.append(df_temp)
        # logger.info(f"⏳ {count}/{qtde_arquivos} arquivos carregados...")
        # count += 1

    df = pd.concat(lista_df, ignore_index=True)
    tamanho_df = len(df)
    logger.info(f"📑 DataFrame com {tamanho_df} linhas criado...")

    return df


if __name__ == "__main__":
    try:
        pasta = Path("files")
        arquivos = list_files(pasta)
        df = csvs_for_df(arquivos)
        print(df)
    except FileNotFoundError as err:
        print(err)
