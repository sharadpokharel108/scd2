# scd2_customer_first_load.py

from config import Config
from Variable import Variables

v = Variables()
v.set("SCRIPT_NAME", "SCD2_CUSTOMER_FIRST_LOAD")
v.set("TMP_TABLE", "TMP_D_CUSTOMER")
v.set("TGT_TABLE", "TGT_D_CUSTOMER_SCD2")
v.set("TMP_SCHEMA", "TEMP")
v.set("TGT_SCHEMA", "TARGET")
conf = Config(v)

# Insert all rows from TMP to empty target table
insert_query = f"""
INSERT INTO {v.get('TGT_SCHEMA')}.{v.get('TGT_TABLE')} (
    CUSTOMER_ID, CUSTOMER_NAME, SEGMENT, START_DATE, END_DATE, CURRENT_FLAG
)
SELECT
    CUSTOMER_ID,
    CUSTOMER_NAME,
    SEGMENT,
    CURRENT_DATE AS START_DATE,
    NULL AS END_DATE,
    TRUE AS CURRENT_FLAG
FROM {v.get('TMP_SCHEMA')}.{v.get('TMP_TABLE')};
"""
conf.execute_query(insert_query)
print("First load into SCD2 CUSTOMER target completed.")