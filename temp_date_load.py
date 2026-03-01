# temp_date_load.py

from config import Config
from Variable import Variables

v = Variables()
v.set("SCRIPT_NAME", "TEMP_DATE_LOAD")
v.set("TMP_TABLE", "TMP_D_DATE")
v.set("TMP_SCHEMA", "TEMP")
v.set("STG_VIEW", "STG_D_DATE")
v.set("STG_SCHEMA", "STAGE")
conf = Config(v)

# 1️⃣ Create temporary date table
create_tmp_query = f"""
CREATE OR REPLACE TABLE {v.get('TMP_SCHEMA')}.{v.get('TMP_TABLE')} (
    ORDER_DATE DATE,
    SHIP_DATE DATE
);
"""
conf.execute_query(create_tmp_query)
print("Temporary DATE table created.")

# 2️⃣ Truncate temporary table
truncate_tmp_query = f"TRUNCATE TABLE {v.get('TMP_SCHEMA')}.{v.get('TMP_TABLE')}"
conf.execute_query(truncate_tmp_query)
print("Temporary DATE table truncated.")

# 3️⃣ Insert distinct dates from stage view
insert_tmp_query = f"""
INSERT INTO {v.get('TMP_SCHEMA')}.{v.get('TMP_TABLE')} (ORDER_DATE, SHIP_DATE)
SELECT DISTINCT ORDER_DATE, SHIP_DATE
FROM {v.get('STG_SCHEMA')}.{v.get('STG_VIEW')};
"""
conf.execute_query(insert_tmp_query)
print("Data loaded into Temporary DATE table from Stage.")