# temp_product_load.py

from config import Config
from Variable import Variables

v = Variables()
v.set("SCRIPT_NAME", "TEMP_PRODUCT_LOAD")
v.set("TMP_TABLE", "TMP_D_PRODUCT")
v.set("STG_VIEW", "STG_D_PRODUCT")
v.set("TMP_SCHEMA", "TEMP")
v.set("STG_SCHEMA", "STAGE")
conf = Config(v)

# Create temporary table
create_tmp_query = f"""
CREATE OR REPLACE TABLE {v.get('TMP_SCHEMA')}.{v.get('TMP_TABLE')} (
    PRODUCT_ID VARCHAR,
    PRODUCT_NAME VARCHAR,
    CATEGORY VARCHAR,
    SUB_CATEGORY VARCHAR
);
"""
conf.execute_query(create_tmp_query)
print("Temporary PRODUCT table created.")

# Truncate temporary table (fresh load)
truncate_tmp_query = f"TRUNCATE TABLE {v.get('TMP_SCHEMA')}.{v.get('TMP_TABLE')}"
conf.execute_query(truncate_tmp_query)
print("Temporary PRODUCT table truncated.")

# Insert distinct rows from stage view
insert_tmp_query = f"""
INSERT INTO {v.get('TMP_SCHEMA')}.{v.get('TMP_TABLE')} (PRODUCT_ID, PRODUCT_NAME, CATEGORY, SUB_CATEGORY)
SELECT DISTINCT PRODUCT_ID, PRODUCT_NAME, CATEGORY, SUB_CATEGORY
FROM {v.get('STG_SCHEMA')}.{v.get('STG_VIEW')};
"""
conf.execute_query(insert_tmp_query)
print("Data loaded into Temporary PRODUCT table from Stage.")