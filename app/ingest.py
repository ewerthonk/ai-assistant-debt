# Imports
import sqlite3
import pandas as pd
from pathlib import Path

# Constants
DATA_FILE_PATH = (
    Path(__file__)
    .parent.parent.joinpath("data")
    .joinpath("raw")
    .joinpath("2024_case_cientista_de_dados_ia.csv")
)
DATABASES_PATH = Path(__file__).parent.parent.joinpath("data").joinpath("databases")

# Data schema
data_file_data_types = {
    "consumidor_id": "int64",
    "cpf_cnpj": "string",
    "nome do consumidor": "string",
    "perfil": "string",
    "divida_id": "string",
    "código_contrato": "string",
    "valor_vencido": "float64",
    "valor_multa": "float64",
    "valor_juros": "float64",
    "produto": "string",
    "loja": "string",
    "Opcoes_Pagamento": "string",
}

# Ingesting datas do DataFrame
df = (
    pd.read_csv(
        filepath_or_buffer=DATA_FILE_PATH,
        dtype=data_file_data_types,
        parse_dates=["data_nascimento", "data_origem"],
        dayfirst=True,
        decimal=",",
    )
    # Handling 10 digit CPF cases
    .assign(cpf_cnpj= lambda _df: _df["cpf_cnpj"].str.zfill(11))
)

# Connection to database (SQLite)
info_db_connection = sqlite3.connect(
    DATABASES_PATH.joinpath("info.db"), check_same_thread=False
)

# Writing table to database
df.to_sql(name="customers", con=info_db_connection, if_exists="replace", index=False)
