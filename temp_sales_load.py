# temp_sales_load.py

from config import Config
from Variable import Variables

v = Variables()
v.set("SCRIPT_NAME", "TEMP_SALES_LOAD")
v.set("TMP_TABLE", "TMP_F_SALES")
v.set("STG_VIEW", "STG_F_SALES")
v.set("TMP_SCHEMA", "TEMP")
v.set("STG_SCHEMA", "STAGE")
conf = Config(v)

# 1️⃣ Create temporary fact table
create_tmp_query = f"""
CREATE OR REPLACE TABLE {v.get('TMP_SCHEMA')}.{v.get('TMP_TABLE')} (
    ORDER_ID VARCHAR,
    CUSTOMER_KEY NUMBER,
    PRODUCT_KEY NUMBER,
    LOCATION_KEY NUMBER,
    ORDER_DATE_KEY NUMBER,
    SHIP_DATE_KEY NUMBER,
    SHIP_MODE_KEY NUMBER,
    QUANTITY FLOAT,
    DISCOUNT FLOAT,
    REVENUE FLOAT,
    PROFIT FLOAT,
    COST FLOAT
);
"""
conf.execute_query(create_tmp_query)
print("Temporary SALES fact table created.")

# 2️⃣ Truncate temporary table
truncate_tmp_query = f"TRUNCATE TABLE {v.get('TMP_SCHEMA')}.{v.get('TMP_TABLE')}"
conf.execute_query(truncate_tmp_query)
print("Temporary SALES fact table truncated.")