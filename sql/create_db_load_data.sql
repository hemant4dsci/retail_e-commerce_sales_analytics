-- Execute below queries step by step to create database and then table.

-- Creating database
CREATE DATABASE IF NOT EXISTS walmart_sales;

-- Choosing the database
USE walmart_sales;

-- Creating calender table
CREATE TABLE calender (
    dates DATE PRIMARY KEY,
    years YEAR,
    half_year CHAR(2),
    quarters CHAR(2),
    months VARCHAR(255),
    weeks VARCHAR(255),
    is_work_day VARCHAR(255),
    europe_session VARCHAR(255),
    north_america_session VARCHAR(255),
    asia_session VARCHAR(255)
);

-- Insert data in calender table
LOAD DATA INFILE '../data/raw/calender.csv'
INTO TABLE calender
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


-- Creating channel table
CREATE TABLE channels (
    channel_key INTEGER PRIMARY KEY,
    channel_name VARCHAR(255)
);

-- Insert data in channel table
LOAD DATA INFILE '../data/raw/channel.csv'
INTO TABLE channels
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


-- Creating geography table
CREATE TABLE geography (
    geo_key INTEGER PRIMARY KEY,
    continent_name VARCHAR(255),
    country_name VARCHAR(255),
    state_province_name VARCHAR(255),
    city_name VARCHAR(255)
);

-- Insert data in geography table
LOAD DATA INFILE '../data/raw/geography.csv'
INTO TABLE geography
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


-- Creating product sub category table
CREATE TABLE product_sub_category (
    product_sub_category_key INTEGER PRIMARY KEY,
    product_sub_category_name VARCHAR(255),
    product_category_name VARCHAR(255)
);

-- Insert data in geography table
LOAD DATA INFILE '../data/raw/product_sub_category.csv'
INTO TABLE product_sub_category
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


-- Creating products table
CREATE TABLE products (
    product_key INTEGER PRIMARY KEY,
    product_name VARCHAR(255),
    brand_name VARCHAR(255),
    class_name VARCHAR(255),
    color_name VARCHAR(255)
);

-- Insert data in geography table
LOAD DATA INFILE '../data/raw/products.csv'
INTO TABLE products
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


-- Creating sales table
CREATE TABLE sales (
    sales_key INTEGER PRIMARY KEY,
    dates DATE,
    channel_key INTEGER,
    product_key INTEGER,
    promotion_key INTEGER,
    geo_key INTEGER,
    product_sub_category_key INTEGER,
    unit_cost DECIMAL(10,2),
    unit_price DECIMAL(10,2),
    sales_quantity INTEGER,
    return_quantity INTEGER,
    return_amount DECIMAL(10,2),
    discount_quantity INTEGER,
    discount_amount DECIMAL(10,2)
);

-- Insert data in geography table
LOAD DATA INFILE '../data/raw/sales.csv'
INTO TABLE sales
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;