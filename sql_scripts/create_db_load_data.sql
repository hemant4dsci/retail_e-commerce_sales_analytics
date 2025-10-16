-- Execute below queries step by step to create database and then table.
-- Creating calender table
CREATE TABLE calender (
    date_key DATE,
    years SMALLINT,
    half_year CHAR(2),
    quarters CHAR(2),
    months VARCHAR(10),
    weeks VARCHAR(10),
    is_work_day VARCHAR(10),
    europe_session VARCHAR(20),
    north_america_session VARCHAR(30),
    asia_session VARCHAR(30),
    CONSTRAINT pk_date_key PRIMARY KEY (date_key)
);

-- Insert data in calender table
COPY calender
FROM
    'E:/Data Analytics Projects Projects/walmart_sales_analytics_project/data/raw/calender.csv'
WITH
    (FORMAT CSV, HEADER TRUE, DELIMITER ',');

-- Creating channel table
CREATE TABLE channels (
    channel_key SMALLINT,
    channel_name VARCHAR(10),
    CONSTRAINT pk_channel_key PRIMARY KEY (channel_key)
);

-- Insert data in channel table
COPY channels
FROM
    'E:/Data Analytics Projects Projects/walmart_sales_analytics_project/data/raw/channel.csv'
WITH
    (FORMAT CSV, HEADER TRUE, DELIMITER ',');

-- Creating geography table
CREATE TABLE geographies (
    geo_key SMALLINT,
    continent_name VARCHAR(20),
    city_name VARCHAR(25),
    state_province_name VARCHAR(40),
    country_name VARCHAR(25),
    CONSTRAINT pk_geo_key PRIMARY KEY (geo_Key)
);

-- Insert data in geography table
COPY geographies
FROM
    'E:/Data Analytics Projects Projects/walmart_sales_analytics_project/data/raw/geography.csv'
WITH
    (FORMAT CSV, HEADER TRUE, DELIMITER ',');

-- Creating product sub-category table
CREATE TABLE product_sub_category (
    product_sub_category_key SMALLINT,
    product_sub_category_name VARCHAR(40),
    product_category_name VARCHAR(40),
    CONSTRAINT pk_product_sub_category_key PRIMARY KEY (product_sub_category_key)
);

-- Insert data in product sub-category table
COPY product_sub_category
FROM
    'E:/Data Analytics Projects Projects/walmart_sales_analytics_project/data/raw/product_sub_category.csv'
WITH
    (FORMAT CSV, HEADER TRUE, DELIMITER ',');

-- Creating products table
CREATE TABLE products (
    product_key SMALLINT,
    product_name TEXT,
    brand_name VARCHAR(25),
    class_name VARCHAR(15),
    color_name VARCHAR(15),
    CONSTRAINT pk_product_key PRIMARY KEY (product_key)
);

-- Insert data in products table
COPY products
FROM
    'E:/Data Analytics Projects Projects/walmart_sales_analytics_project/data/raw/products.csv'
WITH
    (FORMAT CSV, HEADER TRUE, DELIMITER ',');

-- Creating sales table
CREATE TABLE sales (
    sales_key INTEGER,
    date_key DATE,
    channel_key SMALLINT,
    product_key SMALLINT,
    geo_key SMALLINT,
    product_sub_category_key SMALLINT,
    unit_cost NUMERIC(7, 2),
    unit_price NUMERIC(7, 2),
    sales_quantity SMALLINT,
    return_quantity SMALLINT,
    return_amount NUMERIC(7, 2),
    discount_quantity SMALLINT,
    discount_amount NUMERIC(7, 2),
    CONSTRAINT pk_sales_key PRIMARY KEY (sales_key),
    CONSTRAINT fk_date_key FOREIGN KEY (date_key) REFERENCES calender (date_key),
    CONSTRAINT fk_channel_key FOREIGN KEY (channel_key) REFERENCES channels (channel_key),
    CONSTRAINT fk_product_key FOREIGN KEY (product_key) REFERENCES products (product_key),
    CONSTRAINT fk_geo_key FOREIGN KEY (geo_key) REFERENCES geographies (geo_key),
    CONSTRAINT fk_product_sub_category FOREIGN KEY (product_sub_category_key) REFERENCES product_sub_category (product_sub_category_key)
);

-- Insert data in sales table
COPY sales
FROM
    'E:/Data Analytics Projects Projects/walmart_sales_analytics_project/data/raw/sales.csv'
WITH
    (FORMAT CSV, HEADER TRUE, DELIMITER ',');