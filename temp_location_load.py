# temp_location_load.py

from config import Config
from Variable import Variables

v = Variables()
v.set("SCRIPT_NAME", "TEMP_LOCATION_LOAD")
v.set("TMP_TABLE", "TMP_D_LOCATION")
v.set("STG_VIEW", "STG_D_LOCATION")
v.set("TMP_SCHEMA", "TEMP")
v.set("STG_SCHEMA", "STAGE")
conf = Config(v)

# 1️⃣ Create temporary table
create_tmp_query = f"""
CREATE OR REPLACE TABLE {v.get('TMP_SCHEMA')}.{v.get('TMP_TABLE')} (
    COUNTRY VARCHAR,
    REGION VARCHAR,
    STATE VARCHAR,
    CITY VARCHAR,
    POSTAL_CODE VARCHAR
);
"""
conf.execute_query(create_tmp_query)
print("Temporary LOCATION table created.")

# 2️⃣ Truncate temporary table
truncate_tmp_query = f"TRUNCATE TABLE {v.get('TMP_SCHEMA')}.{v.get('TMP_TABLE')}"
conf.execute_query(truncate_tmp_query)
print("Temporary LOCATION table truncated.")

# 3️⃣ Insert distinct rows from stage view
insert_tmp_query = f"""
INSERT INTO {v.get('TMP_SCHEMA')}.{v.get('TMP_TABLE')} (COUNTRY, REGION, STATE, CITY, POSTAL_CODE)
SELECT DISTINCT COUNTRY, REGION, STATE, CITY, POSTAL_CODE
FROM {v.get('STG_SCHEMA')}.{v.get('STG_VIEW')};
"""
conf.execute_query(insert_tmp_query)
print("Data loaded into Temporary LOCATION table from Stage.")