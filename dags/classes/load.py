import pandas as pd
from sqlalchemy import create_engine

class Load:
    def __init__(self, db_connection: str):
        self.db_connection = db_connection

    def df_to_mysql(self, table_name: str, df: pd.DataFrame):
        try:
            engine = create_engine(self.db_connection)
            df.to_sql(table_name, con=engine, if_exists='append', index=False)
        except Exception as e:
            print(e)