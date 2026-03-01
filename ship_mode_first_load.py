# ship_mode_first_load.py

from config import Config
from Variable import Variables

v = Variables()
v.set("SCRIPT_NAME", "SHIP_MODE_FIRST_LOAD")
v.set("TMP_TABLE", "TMP_D_SHIP_MODE")
v.set("TGT_TABLE", "TGT_D_SHIP_MODE")
v.set("TMP_SCHEMA", "TEMP")
v.set("TGT_SCHEMA", "TARGET")
conf = Config(v)

# Insert all rows from TEMP to TARGET
insert_query = f"""
INSERT INTO {v.get('TGT_SCHEMA')}.{v.get('TGT_TABLE')} (SHIP_MODE)
SELECT DISTINCT SHIP_MODE
FROM {v.get('TMP_SCHEMA')}.{v.get('TMP_TABLE')};
"""
conf.execute_query(insert_query)
print("First load into SHIP_MODE target completed.")