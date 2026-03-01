import snowflake.connector
from Variable import Variables
from Logger import Logger

class Config:
    def __init__(self, v: Variables):
        self.v = v
        script_name = v.get("SCRIPT_NAME") or "Nightly_Batch"
        self.log = Logger(script_name, log_path=v.get("LOG_PATH"))

        self.USER = v.get("USER")
        self.PASSWORD = v.get("PASSWORD")
        self.ACCOUNT = v.get("ACCOUNT")
        self.DATABASE = v.get("DATABASE")
        self.DATA_WAREHOUSE = v.get("WAREHOUSE")

        ctx = snowflake.connector.connect(
            user=self.USER,
            password=self.PASSWORD,
            account=self.ACCOUNT,
            database=self.DATABASE,
            warehouse=self.DATA_WAREHOUSE,
            client_telemetry_enabled=False
        )
        self.cs = ctx.cursor()

    def execute_query(self, query):
        try:
            self.log.message(f"Executing query: {query}")
            self.cs.execute(query)
            try:
                val = self.cs.fetchall()
            except:
                val = []
            self.log.message(f"Query Result: {val}")
            return val
        except Exception as e:
            self.log.error(f"query error: {query}")
            self.log.error(f"Error: {e}")

    def executemany(self, query, params):
        try:
            self.log.message(f"Executing query: {query} . Params: {params} ")
            self.cs.executemany(query, params)
            try:
                val = self.cs.fetchall()
            except:
                val = []
            self.log.message(f"Query Result: {val}")
            return val
        except Exception as e:
            self.log.error(f"query error: {query}")
            self.log.error(f"Error: {e}")