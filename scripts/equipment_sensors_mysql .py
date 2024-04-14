import os
import sys


projeto_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(projeto_path)

from classes.load import Load
from credentials.credential import DB, PWD, USER, HOST
from credentials.tables import EQUIPMENT_SENSORS
from classes.extract import Extract
from credentials.paths import PATH_JSON_EQUIP_SENSOR

df = Extract(PATH_JSON_EQUIP_SENSOR).to_dataframe()

df[['equipment_id', 'sensor_id']] = df['item'].str.split(',', expand=True, n=1)
df = df.iloc[1:]
df.drop('item', axis=1, inplace=True)

load = Load(db_connection=f'mysql://{USER}:{PWD}@{HOST}/{DB}')

load.df_to_mysql(table_name=EQUIPMENT_SENSORS,df=df)

print(f'Um total de {len(df)} registros foram carregados na tabela {EQUIPMENT_SENSORS}')