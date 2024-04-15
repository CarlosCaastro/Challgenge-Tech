import os
import sys


projeto_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(projeto_path)


from classes.load import Load
from credentials.credential import DB, PWD, USER, HOST
from credentials.tables import EQUIPMENT
from classes.extract import Extract
from credentials.paths import PATH_JSON_EQUIPMENT

df = Extract(PATH_JSON_EQUIPMENT).to_dataframe()

load = Load(db_connection=f"mysql://{USER}:{PWD}@{HOST}/{DB}")

load.df_to_mysql(table_name=EQUIPMENT, df=df)

print(f"Um total de {len(df)} registros foram carregados na tabela {EQUIPMENT}")
