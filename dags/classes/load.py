import pandas as pd
from sqlalchemy import create_engine


class Load:
    def __init__(self, db_connection: str):
        self.db_connection = db_connection
        self.engine = create_engine(db_connection)
        self.connection = self.engine.raw_connection()

    def close_connection(self):
        self.engine.dispose()
        print("Conexão fechada")

    def df_to_mysql(self, table_name: str, df: pd.DataFrame, schema: str = None):
        try:
            df.to_sql(
                table_name,
                con=self.engine,
                schema=schema,
                if_exists="append",
                index=False,
            )
            print(f"DataFrame inserido na tabela {table_name}")
        except Exception as e:
            print(f"Erro ao inserir DataFrame na tabela {table_name}: {e}")
