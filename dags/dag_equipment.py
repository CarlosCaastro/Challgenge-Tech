from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from classes.load import Load
from credentials.credential import DB, PWD, USER, CONTAINER, PORT
from credentials.tables import EQUIPMENT
from classes.extract import Extract
from credentials.paths import PATH_JSON_EQUIPMENT

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 4, 14),
    "email_on_failure": False,
    "email_on_retry": False,
}

dag = DAG(
    "extract_and_load_equipment",
    default_args=default_args,
    description="Extração de dados seguida por carga no MySQL",
    schedule_interval="@daily",
    catchup=False,
)


def extract_to_dataframe():
    print(PATH_JSON_EQUIPMENT)
    df = Extract(PATH_JSON_EQUIPMENT).to_dataframe()
    return df


def load_to_mysql(**kwargs):
    df = kwargs["ti"].xcom_pull(task_ids="extract_task")
    load = Load(db_connection=f"mysql://{USER}:{PWD}@{CONTAINER}:{PORT}/{DB}")
    load.df_to_mysql(table_name="EQUIPMENT", df=df)


extract_task = PythonOperator(
    task_id="extract_task", python_callable=extract_to_dataframe, dag=dag
)

load_task = PythonOperator(
    task_id="load_task", python_callable=load_to_mysql, provide_context=True, dag=dag
)

extract_task >> load_task
