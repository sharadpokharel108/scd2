# location_first_load.py

from config import Config
from Variable import Variables

# Initialize variables and config
v = Variables()
v.set("SCRIPT_NAME", "LOCATION_FIRST_LOAD")
v.set("TMP_TABLE", "TMP_D_LOCATION")
v.set("TGT_TABLE", "TGT_D_LOCATION")
v.set("TMP_SCHEMA", "TEMP")
v.set("TGT_SCHEMA", "TARGET")
conf = Config(v)

# Insert all rows from TEMP to TARGET
insert_query = f"""
INSERT INTO {v.get('TGT_SCHEMA')}.{v.get('TGT_TABLE')} (
    COUNTRY, REGION, STATE, CITY, POSTAL_CODE
)
SELECT DISTINCT COUNTRY, REGION, STATE, CITY, POSTAL_CODE
FROM {v.get('TMP_SCHEMA')}.{v.get('TMP_TABLE')};
"""
conf.execute_query(insert_query)
print("First load into LOCATION target completed.")