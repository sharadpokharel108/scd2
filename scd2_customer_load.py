# scd2_customer_load.py

from config import Config
from Logger import Logger
from Variable import Variables

v = Variables()
v.set("SCRIPT_NAME", "SCD2_CUSTOMER_LOAD")
# v.set("LOG", Logger(v))
v.set("TMP_TABLE", "TMP_D_CUSTOMER")
v.set("TGT_TABLE", "TGT_D_CUSTOMER_SCD2")
v.set("TMP_SCHEMA", "TEMP")
v.set("TGT_SCHEMA", "TARGET")
conf = Config(v)

# 1️⃣ End-date old records if values changed
update_old_query = f"""
UPDATE {v.get('TGT_SCHEMA')}.{v.get('TGT_TABLE')} tgt
SET END_DATE = CURRENT_DATE - 1,
    CURRENT_FLAG = FALSE
FROM {v.get('TMP_SCHEMA')}.{v.get('TMP_TABLE')} tmp
WHERE tgt.CUSTOMER_ID = tmp.CUSTOMER_ID
  AND tgt.CURRENT_FLAG = TRUE
  AND (tgt.CUSTOMER_NAME != tmp.CUSTOMER_NAME OR tgt.SEGMENT != tmp.SEGMENT);
"""
conf.execute_query(update_old_query)
print("Old CUSTOMER records updated for SCD2.")

# 2️⃣ Insert new records for changes or new customers
insert_new_query = f"""
INSERT INTO {v.get('TGT_SCHEMA')}.{v.get('TGT_TABLE')} (CUSTOMER_ID, CUSTOMER_NAME, SEGMENT)
SELECT tmp.CUSTOMER_ID, tmp.CUSTOMER_NAME, tmp.SEGMENT
FROM {v.get('TMP_SCHEMA')}.{v.get('TMP_TABLE')} tmp
LEFT JOIN {v.get('TGT_SCHEMA')}.{v.get('TGT_TABLE')} tgt
    ON tmp.CUSTOMER_ID = tgt.CUSTOMER_ID AND tgt.CURRENT_FLAG = TRUE
WHERE tgt.CUSTOMER_ID IS NULL
   OR tgt.CUSTOMER_NAME != tmp.CUSTOMER_NAME
   OR tgt.SEGMENT != tmp.SEGMENT;
"""
conf.execute_query(insert_new_query)
print("New CUSTOMER records inserted for SCD2.")

# v.get('LOG').close()
