import pandas as pd
import logging
from sqlalchemy import Column, INTEGER, NUMERIC, VARCHAR, DATE, CHAR
from sqlalchemy.orm import declarative_base

logging.basicConfig(
    filename="../configs/project_logger.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    filemode="w",
)

logger = logging.getLogger(__name__)  # module level logger

# Base class for ORM
Base = declarative_base()


# Defining table as a class
class SalesSummary(Base):
    __tablename__ = "sales_summary"

    # Columns
    id = Column(INTEGER, primary_key=True, autoincrement=True)  # Primary key
    dates = Column(DATE)
    years = Column(INTEGER)
    quarters = Column(CHAR(2))
    months = Column(VARCHAR(255))
    channel_name = Column(VARCHAR(255))
    brand_name = Column(VARCHAR(255))
    class_name = Column(VARCHAR(255))
    continent_name = Column(VARCHAR(255))
    country_name = Column(VARCHAR(255))
    state_province_name = Column(VARCHAR(255))
    product_category_name = Column(VARCHAR(255))
    product_sub_category_name = Column(VARCHAR(255))
    unit_cost = Column(NUMERIC(10, 2))
    unit_price = Column(NUMERIC(10, 2))
    sales_quantity = Column(INTEGER)
    return_quantity = Column(INTEGER)
    return_amount = Column(NUMERIC(10, 2))
    discount_quantity = Column(INTEGER)
    discount_amount = Column(NUMERIC(10, 2))
    total_cost = Column(NUMERIC(15, 2))
    total_sales = Column(NUMERIC(15, 2))
    net_sales = Column(NUMERIC(15, 2))
    net_profit = Column(NUMERIC(15, 2))


def create_sales_summary(engine):
    # This function will merge the diffarent tables to get the overall Sales Summary

    logger.info("Started Sales Summary creation")

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
    except Exception as exc:
        logger.error("Error executing SQL queries: %s", str(exc))

    logger.info("Data cleaning Started")

    # Replacing missing value with 0
    try:
        df.fillna(0, inplace=True)
        logger.info("Replaced the missing value with 0")
    except Exception as exc:
        logger.error("Error filling missing value", str(exc))

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
    except Exception as exc:
        logger.error("Error while removing extra spaces", str(exc))

    # Now creating some new columns or features for better analysis
    try:
        df["total_cost"] = (df["unit_cost"] * df["sales_quantity"]).round(2)
        df["total_sales"] = (df["unit_price"] * df["sales_quantity"]).round(2)
        df["net_sales"] = (
            df["total_sales"] - (df["return_amount"] + df["discount_amount"])
        ).round(2)
        df["net_profit"] = (df["net_sales"] - df["total_cost"]).round(2)
        logger.info("Created new columns successfully")
    except Exception as exc:
        logger.error("Error while creating new columns", str(exc))

    # Creating Table in Database
    try:
        Base.metadata.drop_all(engine)  # Drop old table
        Base.metadata.create_all(engine)  # Create new table
        logger.info("empty sales_summary table created in Data-Base")
    except Exception as exc:
        logger.error("Error creating table in Date-Base: %s", str(exc))

    # Inserting data in the newly created empty table
    try:
        df.to_sql(
            name="sales_summary",
            con=engine,
            if_exists="append",
            index=False,
        )
        logger.info("Data-Frame inserted in sales_summary table successfully")
    except Exception as exc:
        logger.error("Error inserting data into sales_summary table: %s", str(exc))

    logger.info("sales_summary table created in Data-Base successfully")

    return "ETL Process is completed successfully"
