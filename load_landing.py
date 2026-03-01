from config import Config
from Variable import Variables

v = Variables()
conf = Config(v)

# 1️⃣ Create file format
file_format_query = f"""
CREATE OR REPLACE FILE FORMAT {v.get("LND_SCHEMA")}.CSV_FORMAT
TYPE = 'CSV'
FIELD_OPTIONALLY_ENCLOSED_BY = '"'
SKIP_HEADER = 1;
"""
conf.execute_query(file_format_query)

print("File Format Created.")


# 2️⃣ Copy data into SALES table
copy_query = f"""
COPY INTO {v.get("LND_SCHEMA")}.SALES
FROM @{v.get("LND_SCHEMA")}.{v.get("FILE_STAGE")}
FILE_FORMAT = (FORMAT_NAME = {v.get("LND_SCHEMA")}.CSV_FORMAT)
ON_ERROR = 'CONTINUE';
"""
result = conf.execute_query(copy_query)

print("COPY INTO Result:", result)
print("Data Load Attempted.")