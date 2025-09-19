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
LOAD DATA INFILE 'E:/Data Sets/E-Commerce Vendor Data/calender.csv'
INTO TABLE brands
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;