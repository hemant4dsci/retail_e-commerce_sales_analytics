# WalMart Data Analytics Project

**This project explores sales and profitability in the retail and e-commerce sector. The company has enjoyed steady sales growth, but profit margins have not kept pace. Management is particularly concerned about the impact of product returns, aggressive discounting, and uneven regional performance. Our analysis takes a closer look at these challenges by breaking down profitability across products, geographies, and sales channels, while also examining trends over time. The findings highlight where revenue is leaking and provide practical recommendations the business can act on to strengthen margins and support sustainable growth.**

---

>## Table of Contents

+ [Project Objective](#-project-objective)
+ [Project Files](#-project-files)
+ [Project Tree](#-project-tree)
+ [Workflow](#-workflow)
  - [1. Python (Data Cleaning & Fact + Keyword Table Creation)](#-1-python-data-cleaning--fact--keyword-table-creation)
  - [2. Excel (Other Dimension Table Generation)](#-2-excel-other-dimension-table-generation)
  - [3. MySQL (Fact Table Structure First, Then Imports & Keys)](#-3-mysql-fact-table-structure-first-then-imports--keys)
  - [4. Power BI (Visualization, Modeling & DAX)](#-4-power-bi-visualization-modeling--dax)
+ [Data Model Overview](#-data-model-overview)
+ [Tools Used](#️-tools-used)
+ [Key Features](#-key-features)
+ [License](#-license)
+ [Contributing](#-contributing)
+ [Author](#-author)

---

>## Project Objective

The project aims to:

+ Analyze sales and profitability drivers across product categories, brands, and channels.

+ Evaluate the financial impact of returns and discounts on net sales and net profit.

+ Compare regional and geographical performance to highlight markets with high sales but low profitability.

+ Identify trends and seasonality in sales and profit margins across years and quarters.

+ Highlight actionable insights and recommendations to improve overall profitability.

---

>## Project Files

### 1. Data Files

+ Fact Tables
    - `data/raw/sales.csv` – Sales Transactions Table

+ Dimension Tables
    - `data/raw/calendar.csv` – Dates Table
    - `data/raw/channel.csv` – Sales Channel Table
    - `data/raw/geography.csv` – Country and Continent Table
    - `data/raw/product_sub_category.csv` – Product Sub-Category Table
    - `data/raw/products.csv` – Product Details Table

---

### 2. Scripts & Notebooks

+ `sql/create_db_load_data.sql` – SQL script to create database and load tables
+ `scripts/db_sql_etl_process.py` – Executes the full ETL process
+ `scripts/report_generator.py` – Generates summary reports automatically
+ `notebooks/01_db_etl_execute.ipynb` – Notebook to execute ETL process
+ `notebooks/02_exploratory_data_analysis.ipynb` – Performs Exploratory Data Analysis

---

### 3. Reports

+ Dashboards
    - `reports/dashboards/walmart_sales_analysis_dashboard.pbix` – Power BI dashboard
+ Figures
    - `reports/figures/` – Plots and visualizations, e.g., correlation plots, profit analysis, distributions
+ Summary Reports
    - `reports/summary_reports/main_report.pdf` – PDF report

---

>## 📂 Project Tree

```
walmart_sales_analysis/
│
├─ data/                        # Datasets (raw, interim, final)
│  ├─ final/                    # Final processed data
│  ├─ interim/                  # Intermediate cleaned data
│  └─ raw/                      # Raw data sources
│     ├─ calendar.csv                       # Dates table
│     ├─ channel.csv                        # Sales channel table
│     ├─ geography.csv                      # Country & continent table
│     ├─ product_sub_category.csv           # Product sub-category table
│     ├─ products.csv                       # Product details table
│     └─ sales.csv                          # Sales transactions (Fact table)
│
├─ logs/                        # Log files for pipeline runs
│
├─ notebooks/                   # Jupyter notebooks
│  ├─ 01_db_etl_execute.ipynb               # ETL process execute
│  └─ 02_exploratory_data_analysis.ipynb    # Exploratory data analysis
│
├─ reports/
│  ├─ dashboards/                           # Power BI dashboards
│  │  └─ walmart_sales_analysis_dashboard.pbix
│  ├─ figures/                              # Visualizations & plots
│  │  ├─ correlation_plot.png
│  │  ├─ discount_return_impact_profit.png
│  │  ├─ distribution_numeric_column.png
│  │  ├─ frequent_category.png
│  │  ├─ margin_distribution_country.png
│  │  ├─ profit_channel.png
│  │  ├─ qtr_profit_margin.png
│  │  ├─ qtr_sales_return_discount.png
│  │  ├─ revenue_margin_country.png
│  │  ├─ sales_profit_brand.png
│  │  ├─ sales_profit_discount_returns_product_category.png
│  │  └─ summary_stats.png
│  └─ summary_reports/          # PDF reports
│     └─ main_report.pdf
│
├─ scripts/                     # Python scripts
│  └─ db_sql_etl_process.py                 # SQL ETL pipeline
│
├─ sql/                         # SQL schema & data load
│  └─ create_db_load_data.sql               # Create database and load tables
│
├─ .gitattributes
├─ .gitignore
├─ LICENCE
├─ README.md
└─ requirements.txt             # Python dependencies

```
---


>## Project Workflow

The project workflow is organized into the following steps:

### 1. Database Creation
+ Execute `sql/create_db_load_data.sql` in MySQL.  
+ This script creates the database schema and loads all **fact** and **dimension** tables:  
    - `sales.csv` (Fact table)  
    - `calendar.csv`, `channel.csv`, `geography.csv`, `product_sub_category.csv`, `products.csv` (Dimension tables)  

### 2. ETL Process
+ The script extracts raw data, loads it into the database, and applies transformations to prepare structured table.  
+ For interactive execution, open `notebooks/01_db_etl_execute.ipynb` and **execute every cell in order**:
    - One of the notebook cells imports and calls a custom function from `scripts/db_sql_etl_process.py` which runs the entire ETL pipeline and creates the consolidated **sales summary** table.
    - Example (pseudo-code of that cell):
  
    ```python
    import sys

    sys.path.append("../scripts")
    from db_sql_etl_process import create_sales_summary

    create_sales_summary(engine)
    ```

### 3. Exploratory Data Analysis (EDA)  
- Open and run each cell of `notebooks/02_exploratory_data_analysis.ipynb` step by step to explore the cleaned and transformed data.  
- The notebook provides a detailed investigation of sales and profitability patterns through:  

#### Summary Statistics
- Key metrics for **Sales, Net Sales, Returns, Discounts, Cost, Net Profit, and Profit Margin**.  
- Example visualization:  
  ![Summary Statistics](reports/figures/summary_stats.png)

#### Univariate Analysis
- Distribution of **Returns, Discounts, Cost, Net Sales, Net Profit, and Profit Margin** using histograms.  
- Identification of the **most frequent Product Categories and Brands**.

#### Bivariate Analysis
- **Correlation analysis** – quantifies relationships between sales, returns, discounts, and profitability.  
  ![Correlation Plot](reports/figures/correlation_plot.png)  
- **Sales channel profitability analysis** – identifies which **sales channels** generate the highest **profit and margins**.  
- **Product Category Contribution Analysis** – evaluates the percentage contribution of each **Product Category** to overall metrics.  
- **Impact of discounts and returns on profitability** – analyzes how **discount amounts** and **return amounts** affect overall **profit and margins**.  
- **Sales vs Profit Margin across all countries** – compares revenue and profitability performance across different geographies.

#### Time-Series Analysis 
- **Impact of returns and discounts on sales over time** – analyzes how **return amounts** and **discount amounts** influence **sales trends**.  
- **Profit margin trends over time** – tracks whether **profit margins** are improving or declining.  
- Example visualization:  
  ![Quarterly Sales, Returns, Discounts](reports/figures/qtr_sales_ruturn_discount.png)

#### Hypothesis Testing
- **Profit margin variation across countries** – ANOVA test was performed to determine if **profit margins significantly differ among countries**.  
  - **Result:** There is **no significant difference** in profit margins among countries.  
  - **Interpretation:** Since the **p-value is greater than the significance level (α)**, we **fail to reject the null hypothesis**, indicating that profit margins are statistically similar across countries.


> For a summary of actionable insights derived from this analysis, see the **Key Insights** section below.



### 4. Visualization & Dashboards 

+ Visualizations
    + All visualizations generated during the EDA are saved in:  
        - `reports/figures/`
    + These include summary statistics plots, histograms, correlation and bivariate plots, time-series trends, and discount/return impact visualizations.

+ Dashboard
    + Use Power BI dashboard (`reports/dashboards/walmart_sales_analysis_dashboard.pbix`) to visualize insights.  
    + Covers sales trends, profitability, country-level performance, and channel comparisons.
   
### 5. Reporting 

- The final report, including all visuals and detailed analysis, is documented in `reports/summary_reports/main_report.pdf`.  
- Visuals and plots are included to support insights and recommendations.
  

---

## 🧩 Data Model Overview

| Table Name              | Type         | Description                                | Key Field     | Created Using |
|-------------------------|--------------|--------------------------------------------|---------------|----------------|
| `website_traffic_data`  | Fact Table   | Keyword-level AdWords traffic metrics      | `keyword_id`  | Python          |
| `keyword`               | Dimension    | Keyword ID and name mapping                | `keyword_id`  | Python          |
| `competition`           | Dimension    | Keyword competition scores                 | `keyword_id`  | Excel           |
| `keyword_difficulty`    | Dimension    | Keyword difficulty ratings                 | `keyword_id`  | Excel           |

---

## 🛠️ Tools Used

| Tool/Library        | Purpose                                                                 |
|---------------------|-------------------------------------------------------------------------|
| **Python**           | Assign `keyword_id`, create fact and keyword dimension tables           |
| **Jupyter Notebook** | Interactive Python code and data processing                             |
| **Pandas**           | Data manipulation and cleaning                                          |
| **NumPy**            | Numerical transformation support                                        |
| **Excel**            | Create `competition` and `keyword_difficulty` dimension tables          |
| **MySQL**            | Define fact table structure first, then import data & enforce relations |
| **Power BI**         | Build dashboards, model schema, and use DAX for reporting               |

---

## ✅ Key Features
- Assign and manage keyword IDs using Python  
- Build normalized relational structure in MySQL  
- Use Excel for additional dimension data  
- Apply schema constraints and validate relationships with ER diagrams  
- Model and visualize insights in Power BI with custom DAX measures

---

## 🚀 How to Use
1. Run Python notebook to generate:
   - `data/final/website_traffic_data.csv`  
   - `data/final/keyword.csv`  
2. Create `data/final/competition.csv` and `data/final/keyword_difficulty.csv` in Excel  
3. In MySQL:
   - Create structure for `website_traffic_data` first  
   - Import all `.csv` files  
   - Run `sql/traffic_data_script.sql` to define schema and constraints  
   - Validate schema with ERD view  
4. Connect Power BI to MySQL  
5. Model the data and use DAX to create KPIs and dashboards

---

## 📜 License

This project is licensed under the MIT License.

---

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

---

## 👤 Author

Hi, I'm Hemant, a data enthusiast passionate about turning raw data into meaningful business insights.

📫 **Let’s connect:**
- LinkedIn : [LinkedIn Profile](https://www.linkedin.com/in/hemant1491/)  
- Email : hemant4dsci@gmail.com

---

