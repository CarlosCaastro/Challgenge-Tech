import os
import sys
import pandas as pd


projeto_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(projeto_path)

from classes.load import Load
from credentials.credential import DB, PWD, USER, HOST
from credentials.tables import EQUIPMENT_FAILURE_SENSORS
from classes.extract import Extract
from credentials.paths import PATH_JSON_EQUIPMENT_FAILURE

load = Load(db_connection=f"mysql://{USER}:{PWD}@{HOST}/{DB}")

df = Extract(PATH_JSON_EQUIPMENT_FAILURE).to_dataframe()
df["timestamp"] = df["item"].str.extract(r"\[(.*?)\]", expand=False)
df["log_level"] = df["item"].str.extract(r"\b(ERROR|WARNING)\b", expand=False)
df["sensor_id"] = df["item"].str.extract(r"sensor\[(\d+)\]", expand=False).astype(float)
df["temperature"] = (
    df["item"]
    .str.extract(r"temperature\s+([+-]?\d+\.\d+|\d+)", expand=False)
    .astype(float)
)
df["vibration"] = (
    df["item"].str.extract(r"vibration\s+(-?\d+\.\d+|-?\d+)").astype(float)
)
df_sem_duplicatas = df.drop_duplicates(
    subset=["timestamp", "sensor_id", "temperature", "vibration"]
)
load.df_to_mysql(table_name=EQUIPMENT_FAILURE_SENSORS, df=df_sem_duplicatas)
print(
    f"Parte {PATH_JSON_EQUIPMENT_FAILURE} incluida! Contendo {len(df_sem_duplicatas)} registros."
)
