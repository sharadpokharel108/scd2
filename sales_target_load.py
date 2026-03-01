# sales_target_load.py

from config import Config
from Variable import Variables

v = Variables()
v.set("SCRIPT_NAME", "SALES_TARGET_LOAD")
v.set("TMP_TABLE", "TMP_F_SALES")
v.set("TGT_TABLE", "TGT_F_SALES")
v.set("TMP_SCHEMA", "TEMP")
v.set("TGT_SCHEMA", "TARGET")
conf = Config(v)

# 1️⃣ Truncate TARGET fact table (if needed for fresh load)
truncate_tgt_query = f"TRUNCATE TABLE {v.get('TGT_SCHEMA')}.{v.get('TGT_TABLE')}"
conf.execute_query(truncate_tgt_query)
print("TARGET SALES fact table truncated.")

# 2️⃣ Insert all rows from TEMP fact table into TARGET
insert_tgt_query = f"""
INSERT INTO {v.get('TGT_SCHEMA')}.{v.get('TGT_TABLE')} (
    ORDER_ID, CUSTOMER_KEY, PRODUCT_KEY, LOCATION_KEY, ORDER_DATE_KEY,
    SHIP_DATE_KEY, SHIP_MODE_KEY, QUANTITY, DISCOUNT, REVENUE, PROFIT, COST
)
SELECT *
FROM {v.get('TMP_SCHEMA')}.{v.get('TMP_TABLE')};
"""
conf.execute_query(insert_tgt_query)
print("SALES fact table loaded into TARGET.TGT_F_SALES.")