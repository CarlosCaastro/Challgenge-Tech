from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from credentials.credential import DB, PWD, USER, CONTAINER, PORT
from classes.mysql_conn import MySQL
from sqlalchemy import inspect

def get_all_tables_from_db():
    conn = MySQL(db_connection=f'mysql://{USER}:{PWD}@{CONTAINER}:{PORT}/{DB}')
    conn.get_tables()

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 4, 14)
}

dag = DAG(
    'get_all_tables_from_db',
    default_args=default_args,
    description='Retorna todas as tabelas do banco de dados',
    schedule_interval=None
)

get_tables_task = PythonOperator(
    task_id='get_all_tables_task',
    python_callable=get_all_tables_from_db,
    dag=dag
)

get_tables_task
