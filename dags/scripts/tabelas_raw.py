import os
import sys

projeto_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(projeto_path)

from classes.mysql_conn import MySQL
from credentials.paths import DIR
from credentials.tables import DDLS
from credentials.credential import DB, PWD, USER, HOST
from utils.ddl import ler_ddl_arquivo


conn = MySQL(db_connection=f'mysql://{USER}:{PWD}@{HOST}/{DB}')

for arquivo in DDLS:
    path = os.path.join(DIR, arquivo)
    ddl = ler_ddl_arquivo(path)
    conn.run_sql(sql=ddl, schema=DB)
    print(f"Tabela {arquivo} criado com sucesso!")
