# Sales Analytics Dashboard

End-to-end Sales Analytics Dashboard built with Python, SQLite, and Streamlit.

Overview
--------
This repository contains a production-quality end-to-end project that generates a realistic retail sales dataset, cleans and persists it to SQLite, runs business analysis queries, and exposes an interactive Streamlit dashboard.

Quickstart
----------
1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Generate data and populate the SQLite database (100k rows):

```bash
python data/generate_data.py --rows 100000
python data/clean_data.py
```

4. Run the Streamlit dashboard:

```bash
streamlit run dashboard/app.py
```

Project layout
--------------
- `data/` : data generation and cleaning scripts, CSVs
- `sql/` : SQL schema and analysis queries
- `notebooks/` : example notebooks for cleaning and EDA
- `dashboard/` : Streamlit app and helper modules
- `images/` : logos and screenshots
- `docs/` : methodology and insights

See `docs/` for methodology and analysis notes.

## Tech Stack
- Python 3.10+
- Pandas / NumPy for data processing
- SQLite for data storage and analysis
- Streamlit for interactive dashboard
- Plotly / Matplotlib / Seaborn for visualizations

## Features
- End-to-end synthetic retail sales data generation (100k+ rows)
- Data cleaning pipeline and SQLite persistence
- KPI cards: Total Revenue, Total Orders, Average Order Value, Total Profit, Profit Margin
- Charts: Monthly Trend, Sales by Category, Sales by Region, Top Products, Top Customers
- Filters: Year, Month, Region, Category

New analytics features
- Year-over-Year (YoY) Sales Growth: compares yearly revenue and shows percentage growth to highlight trends.
- Customer Segmentation (RFM): automatic Recency-Frequency-Monetary analysis that groups customers into segments like Champions, Loyal, Potential, Needs Attention, and At Risk.
- Business Insights panel: auto-generated bullet-point summary of top category, top region, profit margin, and recent YoY growth for the current filters.

## Folder Structure

sales-analytics-dashboard/
│
├── data/             # data generation and cleaning scripts, CSVs
├── sql/              # SQL schema, DB, and analysis queries
├── notebooks/        # example Jupyter notebooks for EDA/cleaning
├── dashboard/        # Streamlit app and helper modules
├── images/           # logos and screenshots
├── docs/             # methodology and insights
├── requirements.txt
├── README.md
└── .gitignore

## Installation
1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Generate data and populate SQLite DB:

```bash
python data/generate_data.py --rows 100000
python data/clean_data.py
```

4. Run the dashboard locally:

```bash
streamlit run dashboard/app.py
```

## Dashboard Preview
![Dashboard Preview](images/dashboard-preview.png)

### YoY Sales Growth
The YoY chart visualizes percentage change in revenue year-to-year to surface growth or decline trends.

### Customer Segmentation (RFM)
The RFM panel automatically computes Recency (days since last purchase), Frequency (number of orders), and Monetary (total spend) per customer, scores each dimension, and assigns a segment label. This helps identify high-value customers and those needing re-engagement.

## Business Insights
- Seasonal trends surface from the Monthly Sales Trend chart; use promo timing accordingly.
- High-revenue categories and top products indicate where to prioritize inventory and marketing.
- Regional profit discrepancies suggest opportunities for pricing or cost optimization.
- A small number of top customers drive disproportionate revenue — consider retention programs.

## Future Enhancements
- Add customer lifetime value (LTV) and churn prediction models using scikit-learn.
- Add geographic heatmap and store-level analysis.
- Add exportable reports and PDF snapshots from the dashboard.
- Add automated unit/integration tests and CI pipeline.
