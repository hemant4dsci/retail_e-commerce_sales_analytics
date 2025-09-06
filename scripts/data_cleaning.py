import pandas as pd
import logging

logging.basicConfig(
    filename="../configs/project_logger.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    filemode="w",
)

logger = logging.getLogger(__name__)  # Module level logger


def clean_vendor_summary(df):
    # This function will clean and add some columns to the data

    logger.info("Data cleaning Started")
    # Replacing missing value with 0
    try:
        df.fillna(0, inplace=True)
        logger.info("Replaced the missing value with 0")
    except Exception as e:
        logger.error("Error filling missing value", str(e))

    # Removing leading and trailing spaces"""
    try:
        df["vendor_name"] = df["vendor_name"].str.strip()
        logger.info("successfully removed extra spaces")
    except Exception as e:
        logger.error("Error while removing extra spaces", str(e))

    # Removing extra Decimal places

    try:
        df["total_purchase"] = round(df["total_purchase"], 2)
        df["total_sales"] = round(df["total_sales"], 2)
        df["total_excise_tax"] = round(df["total_excise_tax"], 2)
        df["total_freight_cost"] = round(df["total_freight_cost"], 2)
        logger.info("Removed some unnecessory decimal places")
    except Exception as e:
        logger.error("Error while removing extra decimal places", str(e))

    # Now creating some new columns or features for better analysis
    try:
        df["gross_profit"] = round(df["total_sales"] - df["total_purchase"], 2)
        df["profit_margin"] = round((df["gross_profit"] / df["total_sales"]) * 100, 2)
        df["stock_turnover"] = round(df["sales_quantity"] / df["purchase_quantity"], 2)
        df["sales_to_purchase_ratio"] = round(
            df["total_sales"] / df["total_purchase"], 2
        )
        logger.info("Create new columns successfully")
    except Exception as e:
        logger.error("Error while creating new columns", str(e))

    logger.info("Successfully cleaned the data")

    return df
