# scd2_product_first_load.py

from config import Config
from Variable import Variables

# Initialize variables and config
v = Variables()
v.set("SCRIPT_NAME", "SCD2_PRODUCT_FIRST_LOAD")
v.set("TMP_TABLE", "TMP_D_PRODUCT")
v.set("TGT_TABLE", "TGT_D_PRODUCT_SCD2")
v.set("TMP_SCHEMA", "TEMP")
v.set("TGT_SCHEMA", "TARGET")
conf = Config(v)

# Insert all rows from TMP to empty target table
insert_query = f"""
INSERT INTO {v.get('TGT_SCHEMA')}.{v.get('TGT_TABLE')} (
    PRODUCT_ID, PRODUCT_NAME, CATEGORY, SUB_CATEGORY,
    START_DATE, END_DATE, CURRENT_FLAG
)
SELECT
    PRODUCT_ID,
    PRODUCT_NAME,
    CATEGORY,
    SUB_CATEGORY,
    CURRENT_DATE AS START_DATE,
    NULL AS END_DATE,
    TRUE AS CURRENT_FLAG
FROM {v.get('TMP_SCHEMA')}.{v.get('TMP_TABLE')};
"""
conf.execute_query(insert_query)
print("First load into SCD2 PRODUCT target completed.")