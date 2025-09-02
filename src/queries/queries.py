import duckdb
import pandas as pd

df = pd.read_csv("src/queries/data.csv", parse_dates=["time"])
duckdb.register("raw_data", df)

def filtro_data(year=None, month=None, day=None) -> str:
    conds = []
    if year is not None:
        conds.append(f"EXTRACT(YEAR FROM time) = {int(year)}")
    if month is not None:
        conds.append(f"EXTRACT(MONTH FROM time) = {int(month)}")
    if day is not None:
        conds.append(f"EXTRACT(DAY FROM time) = {int(day)}")
    return f"WHERE {' AND '.join(conds)}" if conds else ""

def anos_disponiveis():
    query = """
        SELECT DISTINCT EXTRACT(YEAR FROM time)::INT AS year
        FROM raw_data
        ORDER BY year
    """
    return duckdb.query(query).to_df()["year"].tolist()

def meses_disponiveis(year=None):
    where_sql = filtro_data(year=year)
    query = f"""
        SELECT DISTINCT EXTRACT(MONTH FROM time)::INT AS month
        FROM raw_data
        {where_sql}
        ORDER BY month
    """
    dfm = duckdb.query(query).to_df()
    return dfm["month"].tolist()

def dias_disponiveis(year=None, month=None):
    where_sql = filtro_data(year=year, month=month)
    query = f"""
        SELECT DISTINCT EXTRACT(DAY FROM time)::INT AS day
        FROM raw_data
        {where_sql}
        ORDER BY day
    """
    dfd = duckdb.query(query).to_df()
    return dfd["day"].tolist()

# temperatura vs core speed
def temp_vs_speed(year=None, month=None, day=None):
    where_sql = filtro_data(year, month, day)
    query = f"""
        WITH filtered AS (
            SELECT time, core_temp_0, core_speed_0
            FROM raw_data
            {where_sql}
        )
        SELECT
            core_temp_0 as "core temp",
            MIN(core_speed_0)::INTEGER as "core speed",
            'MIN' AS "type"
        FROM filtered
        GROUP BY 1

        UNION ALL

        SELECT
            core_temp_0 as "core temp",
            AVG(core_speed_0)::INTEGER as "core speed",
            'AVG' AS "type"
        FROM filtered
        GROUP BY 1

        UNION ALL

        SELECT
            core_temp_0 as "core temp",
            MAX(core_speed_0)::INTEGER as "core speed",
            'MAX' AS "type"
        FROM filtered
        GROUP BY 1
    """
    return duckdb.query(query).to_df()

# tempo vs temperatura
def time_vs_temp(year=None, month=None, day=None):
    where_sql = filtro_data(year, month, day)
    query = f"""
        WITH filtered AS (
            SELECT time, core_temp_0
            FROM raw_data
            {where_sql}
        )
        SELECT
            EXTRACT(HOUR FROM time) as "time of day",
            MIN(core_temp_0)::INTEGER as "core temp",
            'MIN' AS "type"
        FROM filtered
        GROUP BY 1

        UNION ALL

        SELECT
            EXTRACT(HOUR FROM time) as "time of day",
            AVG(core_temp_0)::INTEGER as "core temp",
            'AVG' AS "type"
        FROM filtered
        GROUP BY 1

        UNION ALL

        SELECT
            EXTRACT(HOUR FROM time) as "time of day",
            MAX(core_temp_0)::INTEGER as "core temp",
            'MAX' AS "type"
        FROM filtered
        GROUP BY 1
    """
    return duckdb.query(query).to_df()

# tempo vs energia
def time_vs_power(year=None, month=None, day=None):
    where_sql = filtro_data(year, month, day)
    query = f"""
        WITH filtered AS (
            SELECT time, cpu_power
            FROM raw_data
            {where_sql}
        )
        SELECT
            EXTRACT(HOUR FROM time) as "time of day",
            MIN(cpu_power)::INTEGER as "cpu power",
            'MIN' AS "type"
        FROM filtered
        GROUP BY 1

        UNION ALL

        SELECT
            EXTRACT(HOUR FROM time) as "time of day",
            AVG(cpu_power)::INTEGER as "cpu power",
            'AVG' AS "type"
        FROM filtered
        GROUP BY 1

        UNION ALL

        SELECT
            EXTRACT(HOUR FROM time) as "time of day",
            MAX(cpu_power)::INTEGER as "cpu power",
            'MAX' AS "type"
        FROM filtered
        GROUP BY 1
    """
    return duckdb.query(query).to_df()

# temperatura vs energia
def temp_vs_power(year=None, month=None, day=None):
    where_sql = filtro_data(year, month, day)
    query = f"""
        WITH filtered AS (
            SELECT core_temp_0, cpu_power
            FROM raw_data
            {where_sql}
        )
        SELECT
            core_temp_0 as "core temp",
            MIN(cpu_power)::INTEGER as "cpu power",
            'MIN' AS "type"
        FROM filtered
        GROUP BY 1

        UNION ALL

        SELECT
            core_temp_0 as "core temp",
            AVG(cpu_power)::INTEGER as "cpu power",
            'AVG' AS "type"
        FROM filtered
        GROUP BY 1

        UNION ALL

        SELECT
            core_temp_0 as "core temp",
            MAX(cpu_power)::INTEGER as "cpu power",
            'MAX' AS "type"
        FROM filtered
        GROUP BY 1
    """
    return duckdb.query(query).to_df()

# média diária de minutos por faixa de temperatura do processador
def faixas_temp(year=None, month=None, day=None):
    where_sql = filtro_data(year, month, day)
    query = f"""
        WITH filtered AS (
            SELECT time, core_temp_0
            FROM raw_data
            {where_sql}
        ),
        minutos_por_dia AS (
            SELECT DATE(time) AS dia, COUNT(time) / 6.0 AS minutos, '<60' AS categoria
            FROM filtered
            WHERE core_temp_0 < 60
            GROUP BY DATE(time)
        UNION ALL
            SELECT DATE(time) AS dia, COUNT(time) / 6.0 AS minutos, '>=60 & <70' AS categoria
            FROM filtered
            WHERE core_temp_0 >= 60 AND core_temp_0 < 70
            GROUP BY DATE(time)
        UNION ALL
            SELECT DATE(time) AS dia, COUNT(time) / 6.0 AS minutos, '>=70 & <80' AS categoria
            FROM filtered
            WHERE core_temp_0 >= 70 AND core_temp_0 < 80
            GROUP BY DATE(time)
        UNION ALL
            SELECT DATE(time) AS dia, COUNT(time) / 6.0 AS minutos, '>=80 & <90' AS categoria
            FROM filtered
            WHERE core_temp_0 >= 80 AND core_temp_0 < 90
            GROUP BY DATE(time)
        UNION ALL
            SELECT DATE(time) AS dia, COUNT(time) / 6.0 AS minutos, '>=90' AS categoria
            FROM filtered
            WHERE core_temp_0 > 90
            GROUP BY DATE(time)
        )
        SELECT
            ROUND(AVG(minutos)) AS "media diaria",
            categoria,
            CASE
                WHEN categoria = '<60' THEN 1
                WHEN categoria = '>=60 & <70' THEN 2
                WHEN categoria = '>=70 & <80' THEN 3
                WHEN categoria = '>=80 & <90' THEN 4
                WHEN categoria = '>=90' THEN 5
            END AS ordernar
        FROM minutos_por_dia
        GROUP BY categoria
        ORDER BY ordernar
    """
    return duckdb.query(query).to_df()