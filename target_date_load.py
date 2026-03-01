# target_date_load.py

from config import Config
from Variable import Variables

v = Variables()
v.set("SCRIPT_NAME", "TARGET_DATE_LOAD")
v.set("TMP_TABLE", "TMP_D_DATE")
v.set("TGT_TABLE", "TGT_D_DATE")
v.set("TMP_SCHEMA", "TEMP")
v.set("TGT_SCHEMA", "TARGET")
conf = Config(v)

# Insert into TARGET.D_DATE from TEMP table
insert_tgt_query = f"""
INSERT INTO {v.get('TGT_SCHEMA')}.{v.get('TGT_TABLE')} (
    DATE_KEY,
    FULL_DATE,
    YEAR,
    QUARTER,
    MONTH,
    MONTH_NAME,
    WEEK,
    DAY,
    DAY_OF_WEEK,
    DAY_NAME,
    IS_WEEKEND
)
SELECT
    TO_NUMBER(TO_CHAR(d, 'YYYYMMDD')) AS DATE_KEY,
    d AS FULL_DATE,
    YEAR(d) AS YEAR,
    QUARTER(d) AS QUARTER,
    MONTH(d) AS MONTH,
    TO_CHAR(d, 'Mon') AS MONTH_NAME,
    WEEK(d) AS WEEK,
    DAY(d) AS DAY,
    DAYOFWEEK(d) AS DAY_OF_WEEK,
    TO_CHAR(d, 'Dy') AS DAY_NAME,
    IFF(DAYOFWEEK(d) IN (0, 6), TRUE, FALSE) AS IS_WEEKEND
FROM (
    SELECT ORDER_DATE AS d FROM {v.get('TMP_SCHEMA')}.{v.get('TMP_TABLE')}
    UNION
    SELECT SHIP_DATE AS d FROM {v.get('TMP_SCHEMA')}.{v.get('TMP_TABLE')}
)
GROUP BY d
ORDER BY d;
"""
conf.execute_query(insert_tgt_query)
print("DATE dimension loaded into TARGET.TGT_D_DATE.")