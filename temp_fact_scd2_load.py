# temp_fact_scd2_load.py

from config import Config
from Variable import Variables

v = Variables()
v.set("SCRIPT_NAME", "TEMP_FACT_LOAD_SCD2")
v.set("TMP_TABLE", "TMP_F_SALES")
v.set("STG_VIEW", "STG_F_SALES")
v.set("TMP_SCHEMA", "TEMP")
v.set("TGT_SCHEMA", "TARGET")
v.set("STG_SCHEMA", "STAGE")
conf = Config(v)

# 1️⃣ Truncate temporary fact table
truncate_tmp_query = f"TRUNCATE TABLE {v.get('TMP_SCHEMA')}.{v.get('TMP_TABLE')}"
conf.execute_query(truncate_tmp_query)
print("Temporary fact table truncated.")

# 2️⃣ Insert with current SCD2 dimension keys
insert_tmp_query = f"""
INSERT INTO {v.get('TMP_SCHEMA')}.{v.get('TMP_TABLE')} (
    ORDER_ID, CUSTOMER_KEY, PRODUCT_KEY, LOCATION_KEY, ORDER_DATE_KEY,
    SHIP_DATE_KEY, SHIP_MODE_KEY, QUANTITY, DISCOUNT, REVENUE, PROFIT, COST
)
SELECT
    f.ORDER_ID,
    c.CUSTOMER_KEY,
    p.PRODUCT_KEY,
    l.LOCATION_KEY,
    od.DATE_KEY AS ORDER_DATE_KEY,
    sd.DATE_KEY AS SHIP_DATE_KEY,
    s.SHIP_MODE_KEY,
    f.QUANTITY,
    f.DISCOUNT,
    f.REVENUE,
    f.PROFIT,
    f.COST
FROM {v.get('STG_SCHEMA')}.{v.get('STG_VIEW')} f
JOIN {v.get('TGT_SCHEMA')}.TGT_D_CUSTOMER_SCD2 c
    ON c.CUSTOMER_ID = f.CUSTOMER_ID AND c.CURRENT_FLAG = TRUE
JOIN {v.get('TGT_SCHEMA')}.TGT_D_PRODUCT_SCD2 p
    ON p.PRODUCT_ID = f.PRODUCT_ID AND p.CURRENT_FLAG = TRUE
JOIN {v.get('TGT_SCHEMA')}.TGT_D_LOCATION l
    ON TRIM(UPPER(l.COUNTRY)) = TRIM(UPPER(f.COUNTRY))
   AND TRIM(UPPER(l.STATE)) = TRIM(UPPER(f.STATE))
   AND TRIM(UPPER(l.CITY)) = TRIM(UPPER(f.CITY))
   AND TRIM(UPPER(l.POSTAL_CODE)) = TRIM(UPPER(f.POSTAL_CODE))
JOIN {v.get('TGT_SCHEMA')}.TGT_D_DATE od
    ON od.FULL_DATE = f.ORDER_DATE
JOIN {v.get('TGT_SCHEMA')}.TGT_D_DATE sd
    ON sd.FULL_DATE = f.SHIP_DATE
JOIN {v.get('TGT_SCHEMA')}.TGT_D_SHIP_MODE s
    ON s.SHIP_MODE = f.SHIP_MODE;
"""
conf.execute_query(insert_tmp_query)
print("Temporary fact table loaded with current SCD2 dimension keys.")