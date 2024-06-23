# Basic Imports
import sqlite3
from typing import Type, Optional
from textwrap import dedent
import pandas as pd

# LangChain Imports
from langchain.pydantic_v1 import BaseModel, Field
from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain.tools import BaseTool

# Local Imports
from ingest import info_db_connection

class BaseSqlLiteTool(BaseModel):
    """Base tool for interacting with SQLite Database."""
    connection: sqlite3.Connection = Field(exclude=True)
    # Pass sqlite3.Connection validation
    class Config(BaseTool.Config):
        pass


class AuthenticateUserInput(BaseModel):
    cpf: str = Field(
        description="string contendo entre 10 e 11 caracteres numéricos referentes ao CPF do usuário."
    )
    data_nascimento: str = Field(
        description="string com a data de nascimento do usuário no formato 'YYYY-MM-DD'"
    )

class AuthenticateUser(BaseSqlLiteTool, BaseTool):
    name: str = "autenticar_usuario"
    description: str = dedent("""\
        Autentica o usuário. 
        Os inputs são o CPF e a data de nascimento do usuário. 
        Output é uma mensagem informando se o CPF não foi encontrado nos cadastros ou se a data de nascimento não está correta para aquele usuário.
        Ou, caso tenha sido encontrado, o output é um pandas.DataFrame
        """
    )
    args_schema: Type[BaseModel] = AuthenticateUserInput
    def _run(
        self, 
        cpf: str,
        data_nascimento: str,
        run_manager: Optional[CallbackManagerForToolRun]=None,
    ) -> bool:
        cursor = self.connection.cursor()
        if not cursor.execute(f"SELECT * FROM customers WHERE cpf_cnpj = '{cpf}'").fetchone():
            cursor.close()
            return "CPF não encontrado no cadastro da empresa. Checar CPF novamente."
        elif not cursor.execute(f"SELECT * FROM customers WHERE cpf_cnpj = '{cpf}' AND DATE(data_nascimento) = '{data_nascimento}'").fetchone():
            cursor.close()
            return "Os dados informados não foram encontrados no sistema. Checar data de nascimento novamente."
        else:
            df = pd.read_sql_query(f"SELECT * FROM customers WHERE cpf_cnpj = '{cpf}' AND DATE(data_nascimento) = '{data_nascimento}'", self.connection)
            cursor.close()
            return df

# Creating tools instances
authenticate_user_tool = AuthenticateUser(connection=info_db_connection)

# Saving lists of all tools by var and name
tools = [authenticate_user_tool]
tools_by_name = {tool.name: tool for tool in tools}