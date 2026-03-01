# sales_first_load.py

from config import Config
from Variable import Variables

v = Variables()
v.set("SCRIPT_NAME", "SALES_FIRST_LOAD")
v.set("TMP_TABLE", "TMP_F_SALES")
v.set("TGT_TABLE", "TGT_F_SALES")
v.set("STG_VIEW", "STG_F_SALES")
v.set("TMP_SCHEMA", "TEMP")
v.set("TGT_SCHEMA", "TARGET")
v.set("STG_SCHEMA", "STAGE")
conf = Config(v)

# Insert rows into temporary fact table with dimension keys
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
JOIN TARGET.TGT_D_CUSTOMER_SCD2 c ON c.CUSTOMER_ID = f.CUSTOMER_ID AND c.CURRENT_FLAG = TRUE
JOIN TARGET.TGT_D_PRODUCT_SCD2 p ON p.PRODUCT_ID = f.PRODUCT_ID AND p.CURRENT_FLAG = TRUE
JOIN TARGET.TGT_D_LOCATION l ON l.COUNTRY = f.COUNTRY
                            AND l.REGION = f.REGION
                            AND l.STATE = f.STATE
                            AND l.CITY = f.CITY
                            AND l.POSTAL_CODE = f.POSTAL_CODE
JOIN TARGET.TGT_D_DATE od ON od.FULL_DATE = f.ORDER_DATE
JOIN TARGET.TGT_D_DATE sd ON sd.FULL_DATE = f.SHIP_DATE
JOIN TARGET.TGT_D_SHIP_MODE s ON s.SHIP_MODE = f.SHIP_MODE;
"""
conf.execute_query(insert_tmp_query)
print("Data loaded into Temporary SALES fact table with dimension keys.")