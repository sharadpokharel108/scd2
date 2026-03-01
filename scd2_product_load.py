# scd2_product_load.py

from config import Config
from Variable import Variables

v = Variables()
v.set("TMP_TABLE", "TMP_D_PRODUCT")
v.set("TGT_TABLE", "TGT_D_PRODUCT_SCD2")
v.set("TMP_SCHEMA", "TEMP")
v.set("TGT_SCHEMA", "TARGET")
conf = Config(v)

# 1️⃣ End-date old records if values changed
update_old_query = f"""
UPDATE {v.get('TGT_SCHEMA')}.{v.get('TGT_TABLE')} tgt
SET END_DATE = CURRENT_DATE - 1,
    CURRENT_FLAG = FALSE
FROM {v.get('TMP_SCHEMA')}.{v.get('TMP_TABLE')} tmp
WHERE tgt.PRODUCT_ID = tmp.PRODUCT_ID
  AND tgt.CURRENT_FLAG = TRUE
  AND (
      tgt.PRODUCT_NAME != tmp.PRODUCT_NAME OR
      tgt.CATEGORY != tmp.CATEGORY OR
      tgt.SUB_CATEGORY != tmp.SUB_CATEGORY
  );
"""
conf.execute_query(update_old_query)
print("Old PRODUCT records updated for SCD2.")

# 2️⃣ Insert new records for changes or new products
insert_new_query = f"""
INSERT INTO {v.get('TGT_SCHEMA')}.{v.get('TGT_TABLE')} (PRODUCT_ID, PRODUCT_NAME, CATEGORY, SUB_CATEGORY)
SELECT tmp.PRODUCT_ID, tmp.PRODUCT_NAME, tmp.CATEGORY, tmp.SUB_CATEGORY
FROM {v.get('TMP_SCHEMA')}.{v.get('TMP_TABLE')} tmp
LEFT JOIN {v.get('TGT_SCHEMA')}.{v.get('TGT_TABLE')} tgt
    ON tmp.PRODUCT_ID = tgt.PRODUCT_ID AND tgt.CURRENT_FLAG = TRUE
WHERE tgt.PRODUCT_ID IS NULL
   OR tgt.PRODUCT_NAME != tmp.PRODUCT_NAME
   OR tgt.CATEGORY != tmp.CATEGORY
   OR tgt.SUB_CATEGORY != tmp.SUB_CATEGORY;
"""
conf.execute_query(insert_new_query)
print("New PRODUCT records inserted for SCD2.")