import pandas as pd
import logging
from sqlalchemy import MetaData, Table, Column, INTEGER, NUMERIC, VARCHAR, DATE, CHAR

logging.basicConfig(
    filename="../configs/project_logger.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    filemode="w",
)

logger = logging.getLogger(__name__)  # module level logger


def create_sales_summary(engine):
    # This function will merge the diffarent tables to get the overall vendor summary

    logger.info("Started sales summary creation")

    summary_query = """
        WITH sales_summary AS(
            SELECT 
                dates,
                channel_key,
                product_key,
                geo_key,
                product_sub_category_key,
                MIN(unit_cost) AS unit_cost,
                MIN(unit_price) AS unit_price,
                SUM(sales_quantity) AS sales_quantity,
                SUM(return_quantity) AS return_quantity,
                SUM(return_amount) AS return_amount,
                SUM(discount_quantity) AS discount_quantity,
                SUM(discount_amount) AS discount_amount
            FROM sales
            GROUP BY 
                dates,
                channel_key,
                product_key,
                geo_key,
                product_sub_category_key
        )
        SELECT
            ss.dates,
            cd.years,
            cd.quarters,
            cd.months,
            ch.channel_name,
            pd.brand_name,
            pd.class_name,
            gg.continent_name,
            gg.country_name,
            gg.state_province_name,
            psc.product_category_name,
            psc.product_sub_category_name,
            ss.unit_cost,
            ss.unit_price,
            ss.sales_quantity,
            ss.return_quantity,
            ss.return_amount,
            ss.discount_quantity,
            ss.discount_amount
        FROM sales_summary ss
        LEFT JOIN calender cd
            ON ss.dates = cd.dates
        LEFT JOIN channels ch
            ON ss.channel_key = ch.channel_key
        LEFT JOIN products pd
            ON ss.product_key = pd.product_key
        LEFT JOIN geography gg
            ON ss.geo_key = gg.geo_key
        LEFT JOIN product_sub_category psc
            ON ss.product_sub_category_key = psc.product_sub_category_key;
    """

    try:
        df = pd.read_sql(sql=summary_query, con=engine)
        logger.info(
            "SQL query executed successfully. retrived %d rows",
            len(df),
        )
    except Exception as e:
        logger.error("Error executing SQL queries: %s", str(e))

    logger.info("Data cleaning Started")

    # Replacing missing value with 0
    try:
        df.fillna(0, inplace=True)
        logger.info("Replaced the missing value with 0")
    except Exception as e:
        logger.error("Error filling missing value", str(e))

    # # Removing leading and trailing spaces
    try:
        for col in [
            "months",
            "channel_name",
            "brand_name",
            "class_name",
            "continent_name",
            "country_name",
            "state_province_name",
            "product_category_name",
            "product_sub_category_name",
        ]:
            df[col] = df[col].astype(str).str.strip()
        logger.info("Successfully removed extra spaces")
    except Exception as e:
        logger.error("Error while removing extra spaces", str(e))

    # Now creating some new columns or features for better analysis
    try:
        df["total_cost"] = (df["unit_cost"] * df["sales_quantity"]).round(2)
        df["total_sales"] = (df["unit_price"] * df["sales_quantity"]).round(2)
        df["net_sales"] = (
            df["total_sales"] - (df["return_amount"] + df["discount_amount"])
        ).round(2)
        df["net_profit"] = (df["net_sales"] - df["total_cost"]).round(2)
        logger.info("Created new columns successfully")
    except Exception as e:
        logger.error("Error while creating new columns", str(e))

    # metadata object keeps track of tables
    metadata = MetaData()

    # Defining the table structure
    create_table = Table(
        "sales_summary",  # table name
        metadata,  # attach to metadata
        Column("dates", DATE),
        Column("years", INTEGER),
        Column("quarters", CHAR(2)),
        Column("months", VARCHAR(255)),
        Column("channel_name", VARCHAR(255)),
        Column("brand_name", VARCHAR(255)),
        Column("class_name", VARCHAR(255)),
        Column("continent_name", VARCHAR(255)),
        Column("country_name", VARCHAR(255)),
        Column("state_province_name", VARCHAR(255)),
        Column("product_category_name", VARCHAR(255)),
        Column("product_sub_category_name", VARCHAR(255)),
        Column("unit_cost", NUMERIC(10, 2)),
        Column("unit_price", NUMERIC(10, 2)),
        Column("sales_quantity", INTEGER),
        Column("return_quantity", INTEGER),
        Column("return_amount", NUMERIC(10, 2)),
        Column("discount_quantity", INTEGER),
        Column("discount_amount", NUMERIC(10, 2)),
        Column("total_cost", NUMERIC(15, 2)),
        Column("total_sales", NUMERIC(15, 2)),
        Column("net_sales", NUMERIC(15, 2)),
        Column("net_profit", NUMERIC(15, 2)),
    )

    # Creating Table in Database
    try:
        metadata.create_all(engine)
        logger.info("empty sales_summary table created in Data-Base")
    except Exception as e:
        logger.error("Error creating table in Date-Base: %s", str(e))

    # Inserting data in the newly created empty table
    try:
        df.to_sql(
            name="sales_summary",
            con=engine,
            if_exists="replace",
            index=False,
        )
        logger.info("Data-Frame inserted in sales_summary table successfully")
    except Exception as e:
        logger.error("Error inserting data into sales_summary table: %s", str(e))

    logger.info("sales_summary table created in Data-Base successfully")

    return "ETL Process is completed successfully"
