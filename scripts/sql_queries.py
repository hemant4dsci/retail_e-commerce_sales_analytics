import pandas as pd
import logging
from sqlalchemy import MetaData, Table, Column, Integer, Numeric, String

logging.basicConfig(
    filename="../configs/get_vendor_summary.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a",
)

def create_vendor_summary(engine):
    """This function will merge the diffrent tables to get the overall vendor summary and adding new columns in the resultant data"""

    summary_query = """
    WITH purchase_summary AS (
        SELECT 
            brand_id,
            vendor_id,
            SUM(purchase_quantity) AS purchase_quantity,
            SUM(total_purchase) AS total_purchase,
            MAX(purchase_price) AS purchase_price
        FROM purchases
        GROUP BY brand_id, vendor_id
    ),
    sales_summary AS (
        SELECT 
            brand_id,
            vendor_id,
            SUM(sales_quantity) AS sales_quantity,
            SUM(total_sales) AS total_sales,
            SUM(excise_tax) AS total_excise_tax,
            MAX(sales_price) AS sales_price
        FROM sales
        GROUP BY brand_id, vendor_id
    ),
    freight_summary AS (
        SELECT 
            vendor_id,
            SUM(freight_cost) AS total_freight_cost
        FROM vendor_invoice
        GROUP BY vendor_id
    )
    SELECT
        p.brand_id,
        p.vendor_id,
        v.vendor_name,
        bp.price AS actual_price,
        p.purchase_price,
        s.sales_price,
        p.purchase_quantity,
        s.sales_quantity,
        p.total_purchase,
        s.total_sales,
        s.total_excise_tax,
        f.total_freight_cost
    FROM purchase_summary p
    LEFT JOIN sales_summary s 
        ON p.vendor_id = s.vendor_id AND p.brand_id = s.brand_id
    LEFT JOIN freight_summary f 
        ON p.vendor_id = f.vendor_id
    LEFT JOIN brand_prices bp 
        ON p.brand_id = bp.brand_id
    LEFT JOIN vendors v 
        ON p.vendor_id = v.vendor_id;
    """
    vendor_purchase_sales = pd.read_sql(sql=summary_query, con=engine)

    # metadata object keeps track of tables
    metadata = MetaData()

    """ Defining the table """
    create_table = Table(
        "vendor_purchase_sales_summary",  # table name
        metadata,  # attach to metadata
        Column("brand_id", Integer, primary_key=True),
        Column("vendor_id", Integer, primary_key=True),
        Column("vendor_name", String(255)),
        Column("actual_price", Numeric(15, 2)),
        Column("purchase_price", Numeric(15, 2)),
        Column("sales_price", Numeric(15, 2)),
        Column("purchase_quantity", Integer),
        Column("sales_quantity", Integer),
        Column("total_purchase", Numeric(15, 2)),
        Column("total_sales", Numeric(15, 2)),
        Column("total_excise_tax", Numeric(15, 2)),
        Column("total_freight_cost", Numeric(15, 2)),
    )

    """ Creating Table in """
    metadata.create_all(engine)

    vendor_purchase_sales.to_sql(
        "vendor_purchase_sales_summary", engine, if_exists="replace", index=False
    )

    return vendor_purchase_sales
