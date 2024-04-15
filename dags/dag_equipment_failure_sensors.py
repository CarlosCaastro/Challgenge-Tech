from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from classes.load import Load
from credentials.credential import DB, PWD, USER, CONTAINER, PORT
from credentials.tables import EQUIPMENT_FAILURE_SENSORS
from classes.extract import Extract
from credentials.paths import PATH_JSON_EQUIPMENT_FAILURE


def extract():
    df = Extract(PATH_JSON_EQUIPMENT_FAILURE).to_dataframe()
    return df


def transform(**kwargs):
    df = kwargs["ti"].xcom_pull(task_ids="extract")
    df["timestamp"] = df["item"].str.extract(r"\[(.*?)\]", expand=False)
    df["log_level"] = df["item"].str.extract(r"\b(ERROR|WARNING)\b", expand=False)
    df["sensor_id"] = (
        df["item"].str.extract(r"sensor\[(\d+)\]", expand=False).astype(float)
    )
    df["temperature"] = (
        df["item"]
        .str.extract(r"temperature\s+([+-]?\d+\.\d+|\d+)", expand=False)
        .astype(float)
    )
    df["vibration"] = (
        df["item"].str.extract(r"vibration\s+(-?\d+\.\d+|-?\d+)").astype(float)
    )
    df = df.drop_duplicates(
        subset=["timestamp", "sensor_id", "temperature", "vibration"]
    )
    return df


def load_to_mysql(**kwargs):
    df = kwargs["ti"].xcom_pull(task_ids="transform")
    load = Load(db_connection=f"mysql://{USER}:{PWD}@{CONTAINER}:{PORT}/{DB}")
    load.df_to_mysql(table_name=EQUIPMENT_FAILURE_SENSORS, df=df)


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2022, 1, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "extract_and_load_equipment_failure_sensors",
    default_args=default_args,
    description="Uma DAG para processamento de dados",
    schedule_interval="@daily",
)

extract_task = PythonOperator(
    task_id="extract_data",
    python_callable=extract,
    dag=dag,
)

transform_task = PythonOperator(
    task_id="transform_data",
    python_callable=transform,
    provide_context=True,
    dag=dag,
)

load_to_mysql_task = PythonOperator(
    task_id="load_to_mysql",
    python_callable=load_to_mysql,
    provide_context=True,
    dag=dag,
)

extract_task >> transform_task >> load_to_mysql_task
