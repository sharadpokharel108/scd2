# sales_target_scd2_load.py

from config import Config
from Variable import Variables

# 1️⃣ Initialize Variables and Config
v = Variables()
v.set("TMP_TABLE", "TMP_F_SALES")
v.set("TMP_SCHEMA", "TEMP")
v.set("TGT_TABLE", "TGT_F_SALES")
v.set("TGT_SCHEMA", "TARGET")
conf = Config(v)

# 2️⃣ Merge TEMP fact table into TARGET fact table
merge_query = f"""
MERGE INTO {v.get('TGT_SCHEMA')}.{v.get('TGT_TABLE')} AS TGT
USING {v.get('TMP_SCHEMA')}.{v.get('TMP_TABLE')} AS TMP
ON TGT.ORDER_ID = TMP.ORDER_ID
WHEN MATCHED THEN
    UPDATE SET 
        TGT.CUSTOMER_KEY = TMP.CUSTOMER_KEY,
        TGT.PRODUCT_KEY = TMP.PRODUCT_KEY,
        TGT.LOCATION_KEY = TMP.LOCATION_KEY,
        TGT.ORDER_DATE_KEY = TMP.ORDER_DATE_KEY,
        TGT.SHIP_DATE_KEY = TMP.SHIP_DATE_KEY,
        TGT.SHIP_MODE_KEY = TMP.SHIP_MODE_KEY,
        TGT.QUANTITY = TMP.QUANTITY,
        TGT.DISCOUNT = TMP.DISCOUNT,
        TGT.REVENUE = TMP.REVENUE,
        TGT.PROFIT = TMP.PROFIT,
        TGT.COST = TMP.COST
WHEN NOT MATCHED THEN
    INSERT (ORDER_ID, CUSTOMER_KEY, PRODUCT_KEY, LOCATION_KEY, ORDER_DATE_KEY,
            SHIP_DATE_KEY, SHIP_MODE_KEY, QUANTITY, DISCOUNT, REVENUE, PROFIT, COST)
    VALUES (TMP.ORDER_ID, TMP.CUSTOMER_KEY, TMP.PRODUCT_KEY, TMP.LOCATION_KEY, TMP.ORDER_DATE_KEY,
            TMP.SHIP_DATE_KEY, TMP.SHIP_MODE_KEY, TMP.QUANTITY, TMP.DISCOUNT, TMP.REVENUE, TMP.PROFIT, TMP.COST);
"""

conf.execute_query(merge_query)
print("TARGET fact table updated with current SCD2 dimension keys.")