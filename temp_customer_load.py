# temp_customer_load.py

from config import Config
from Variable import Variables

# Initialize variables and config
v = Variables()
v.set("SCRIPT_NAME", "TEMP_CUSTOMER_LOAD")
v.set("TMP_TABLE", "TMP_D_CUSTOMER")
v.set("STG_VIEW", "STG_D_CUSTOMER")
v.set("TMP_SCHEMA", "TEMP")
v.set("STG_SCHEMA", "STAGE")
conf = Config(v)

# 1️⃣ Create temporary table (if it doesn't exist)
create_tmp_query = f"""
CREATE OR REPLACE TABLE {v.get('TMP_SCHEMA')}.{v.get('TMP_TABLE')} (
    CUSTOMER_ID VARCHAR,
    CUSTOMER_NAME VARCHAR,
    SEGMENT VARCHAR
);
"""
conf.execute_query(create_tmp_query)
print("Temporary Table Created.")

# 2️⃣ Truncate temporary table (fresh load)
truncate_tmp_query = f"TRUNCATE TABLE {v.get('TMP_SCHEMA')}.{v.get('TMP_TABLE')}"
conf.execute_query(truncate_tmp_query)
print("Temporary Table Truncated.")

# 3️⃣ Insert distinct customer data from stage view
insert_tmp_query = f"""
INSERT INTO {v.get('TMP_SCHEMA')}.{v.get('TMP_TABLE')} (CUSTOMER_ID, CUSTOMER_NAME, SEGMENT)
SELECT DISTINCT CUSTOMER_ID, CUSTOMER_NAME, SEGMENT
FROM {v.get('STG_SCHEMA')}.{v.get('STG_VIEW')};
"""
conf.execute_query(insert_tmp_query)
print("Data loaded into Temporary Table from Stage.")