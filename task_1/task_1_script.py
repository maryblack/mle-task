import psycopg2
import pandas as pd


class ReportKPI:
    DBNAME = 'maryblack'
    USER = 'maryblack'
    PASSWORD = 'maryblack'
    HOST = 'localhost'

    CREATE_TABLE = """
    --DROP TABLE TESTSET_B;
    CREATE TABLE IF NOT EXISTS TESTSET_B (
        PRODUCTID VARCHAR(32),
        BRAND VARCHAR(32),
        RAM_GB NUMERIC,
        HDD_GB NUMERIC,
        GHZ NUMERIC,
        PRICE NUMERIC
    );

    COPY TESTSET_B(PRODUCTID, BRAND, RAM_GB, HDD_GB, GHZ, PRICE)
    FROM '/tmp/testset_B.tsv'
    DELIMITER E'\t'
    CSV HEADER;
    """

    # Ranks based on column Price, grouped by column brand
    SQL_A = """
    SELECT
        PRODUCTID,
        BRAND,
        PRICE,
        HDD_GB,
        GHZ,
        RANK () OVER ( 
            PARTITION BY BRAND
            ORDER BY PRICE DESC
        ) PRICE_RANK 
    FROM TESTSET_B;
    """

    # Minimum and maximum of column HDD_GB
    SQL_B = """
    SELECT
        MIN(HDD_GB) MIN_HDD_GB,
        MAX(HDD_GB) MAX_HDD_GB
    FROM TESTSET_B
    """

    # Median of column GHz, grouped by column RAM_GB
    # since median is the 50th percentile, we can use it as a proxy to median
    SQL_C = """
    SELECT
        RAM_GB, 
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY GHZ) MEDIAN_GHZ
    FROM TESTSET_B
    GROUP BY RAM_GB
    """

    @staticmethod
    def create():
        conn = psycopg2.connect(dbname=ReportKPI.DBNAME,
                                user=ReportKPI.USER,
                                password=ReportKPI.PASSWORD,
                                host=ReportKPI.HOST)

        cursor = conn.cursor()
        cursor.execute(ReportKPI.CREATE_TABLE)
        pd.read_sql(ReportKPI.SQL_A, conn).to_csv("report_A.csv", index=False, sep=";")
        pd.read_sql(ReportKPI.SQL_B, conn).to_csv("report_B.csv", index=False, sep=";")
        pd.read_sql(ReportKPI.SQL_C, conn).to_csv("report_C.csv", index=False, sep=";")


report = ReportKPI()
report.create()
