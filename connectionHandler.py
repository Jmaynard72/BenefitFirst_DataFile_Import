from sqlalchemy import URL
from sqlalchemy import create_engine
import pandas as pd 

class ConnectionHandler:
    def __init__(self, host, database):
        self.host = host 
        self.database = database 

        self.engine = create_engine(f"mssql+pyodbc://@{self.host}/{self.database}?trusted_connection=yes&driver=ODBC+Driver+18+for+SQL+Server")
    def fetch_data(self, query):
        return pd.read_sql(query,self.engine)
    
    def insert_data(self,df,tablename):
        df.to_sql(tablename, if_exits='append', index=False, con=self.db_connection)

    def execute_query(self,query):
        self.db_connection.execute(query)
    
    def __del__(self):
        try:
            self.db_connection.close()
        except:
            None