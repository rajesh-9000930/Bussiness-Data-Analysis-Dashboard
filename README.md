# Business Data Analysis Dashboard

A portfolio-ready sales analytics dashboard built with Python, Pandas, Streamlit and Plotly.

## Features
- KPI cards: revenue, profit, orders, units sold and profit margin
- Interactive filters for date, region, category and sales channel
- Monthly revenue trend
- Revenue by category and region
- Top 10 products by revenue
- Filtered transaction table and CSV export
- Optional upload of another sales CSV using the same column structure

## Run locally
1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Install dependencies:
   `pip install -r requirements.txt`
4. Start the dashboard:
   `streamlit run app.py`
5. Open the local URL printed in the terminal (usually http://localhost:8501).

## Dataset
`business_sales_data.csv` contains 600 synthetic example sales transactions. It is not real Deloitte or client data.

Required columns:
Order_ID, Order_Date, Region, Category, Product, Units_Sold, Unit_Price, Discount, Revenue, Cost, Profit, Channel

## Suggested resume entry (use after you run and understand the project)
**Business Data Analysis Dashboard | Python, Pandas, SQL concepts, Streamlit, Plotly**
- Built an interactive sales analytics dashboard to monitor revenue, profit, order volume and profit margin.
- Cleaned and analyzed 600 sample transactions using Pandas and visualized monthly, regional and category-level performance.
- Added interactive filters and CSV export to support focused analysis and reporting.

Only claim features and tools you have personally tested and can explain in an interview. This starter project uses Pandas for analysis; SQL is listed as a learning extension, not implemented in this version.

## Possible extensions
- Load data from MySQL using SQL queries.
- Add month-over-month growth and year-to-date comparisons.
- Add login and role-based access.
- Deploy on Streamlit Community Cloud.
