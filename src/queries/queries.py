import duckdb
import pandas as pd

df = pd.read_csv("src/queries/data.csv", parse_dates=["time"])
duckdb.register("raw_data", df)

# temperatura vs core speed
def temp_vs_speed():

    query = """
        SELECT
            core_temp_0 as "core temp",
            MIN(core_speed_0)::INTEGER as "core speed",
            'MIN' AS "type"
        FROM raw_data
        GROUP BY 1

        UNION ALL

        SELECT
            core_temp_0 as "core temp",
            AVG(core_speed_0)::INTEGER as "core speed",
            'AVG' AS "type"
        FROM raw_data
        GROUP BY 1

        UNION ALL

        SELECT
            core_temp_0 as "core temp",
            MAX(core_speed_0)::INTEGER as "core speed",
            'MAX' AS "type"
        FROM raw_data
        GROUP BY 1
    """
    return duckdb.query(query).to_df()

# tempo vs temperatura
def time_vs_temp():
    query = """
        SELECT
            EXTRACT(HOUR FROM time) as "time of day",
            MIN(core_temp_0)::INTEGER as "core temp",
            'MIN' AS "type"
        FROM raw_data
        GROUP BY 1

        UNION ALL

        SELECT
            EXTRACT(HOUR FROM time) as "time of day",
            AVG(core_temp_0)::INTEGER as "core temp",
            'AVG' AS "type"
        FROM raw_data
        GROUP BY 1

        UNION ALL

        SELECT
            EXTRACT(HOUR FROM time) as "time of day",
            MAX(core_temp_0)::INTEGER as "core temp",
            'MAX' AS "type"
        FROM raw_data
        GROUP BY 1
    """
    return duckdb.query(query).to_df()

# tempo vs energia
def time_vs_power():
    query = """
        SELECT
            EXTRACT(HOUR FROM time) as "time of day",
            MIN(cpu_power)::INTEGER as "cpu power",
            'MIN' AS "type"
        FROM raw_data
        GROUP BY 1

        UNION ALL

        SELECT
            EXTRACT(HOUR FROM time) as "time of day",
            AVG(cpu_power)::INTEGER as "cpu power",
            'AVG' AS "type"
        FROM raw_data
        GROUP BY 1

        UNION ALL

        SELECT
            EXTRACT(HOUR FROM time) as "time of day",
            MAX(cpu_power)::INTEGER as "cpu power",
            'MAX' AS "type"
        FROM raw_data
        GROUP BY 1
    """
    return duckdb.query(query).to_df()

# temperatura vs energia
def temp_vs_power():
    query = """
        SELECT
            core_temp_0 as "core temp",
            MIN(cpu_power)::INTEGER as "cpu power",
            'MIN' AS "type"
        FROM raw_data
        GROUP BY 1

        UNION ALL

        SELECT
            core_temp_0 as "core temp",
            AVG(cpu_power)::INTEGER as "cpu power",
            'AVG' AS "type"
        FROM raw_data
        GROUP BY 1

        UNION ALL

        SELECT
            core_temp_0 as "core temp",
            MAX(cpu_power)::INTEGER as "cpu power",
            'MAX' AS "type"
        FROM raw_data
        GROUP BY 1
    """
    return duckdb.query(query).to_df()
    
# média diária de minutos por faixa de temperatura do processador
def faixas_temp():
    query = """
            WITH minutos_por_dia AS (
        SELECT
            DATE(time) AS dia,
            COUNT(time) / 6.0 AS minutos,
            '<60' AS categoria
        FROM
            raw_data
        WHERE
            core_temp_0 < 60
        GROUP BY
            DATE(time)
    UNION ALL
        SELECT
            DATE(time) AS dia,
            COUNT(time) / 6.0 AS minutos,
            '>=60 & <70' AS categoria
        FROM
            raw_data
        WHERE
            core_temp_0 >= 60 AND core_temp_0 < 70
        GROUP BY
            DATE(time)
    UNION ALL
        SELECT
            DATE(time) AS dia,
            COUNT(time) / 6.0 AS minutos,
            '>=70 & <80' AS categoria
        FROM
            raw_data
        WHERE
            core_temp_0 >= 70 AND core_temp_0 < 80
        GROUP BY
            DATE(time)
    UNION ALL
        SELECT
            DATE(time) AS dia,
            COUNT(time) / 6.0 AS minutos,
            '>=80 & <90' AS categoria
        FROM
            raw_data
        WHERE
            core_temp_0 >= 80 AND core_temp_0 < 90
        GROUP BY
            DATE(time)
    UNION ALL
        SELECT
            DATE(time) AS dia,
            COUNT(time) / 6.0 AS minutos,
            '>=90' AS categoria
        FROM
            raw_data
        WHERE
            core_temp_0 > 90
        GROUP BY
            DATE(time)
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
    FROM
        minutos_por_dia
    GROUP BY
        categoria
    ORDER BY
        ordernar
    """
    return duckdb.query(query).to_df()