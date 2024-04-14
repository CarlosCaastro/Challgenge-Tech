import pandas as pd
from sqlalchemy import create_engine

class MySQL:
    def __init__(self,db_connection:str):
        self.dbt_connection = db_connection
        self.engine = create_engine(self.dbt_connection)
        self.connection = self.engine.raw_connection()
   
    def close_connection(self):
        self.engine.dispose()
        print('Conexão fechada')

    def run_sql(self, sql: str, schema: str = None):
        sql = f"USE {schema}; {sql}"
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            print('SQL executado')
            cursor.close()
        except Exception as e:
            print(f'Erro: {e}')

    def create_schema(self, schema_name: str):
        cursor = self.connection.cursor()
        cursor.execute(f'CREATE SCHEMA IF NOT EXISTS {schema_name}')
        cursor.close()

    def get_tables(self):
        try:
            query = "SHOW TABLES"
            cursor = self.connection.cursor()
            cursor.execute(query)
            tables = cursor.fetchall()
            cursor.close()
            print("Tabelas:")
            for table in tables:
                print(table[0])
        except Exception as e:
            print(f'Erro ao recuperar as tabelas: {e}')