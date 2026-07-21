import os
import sys
import streamlit as st

# Ensure repository root is on sys.path so absolute imports like
# `from dashboard.data_loader import ...` work when Streamlit runs
# this file as a script (Streamlit Community Cloud behavior).
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from dashboard.data_loader import load_sales_table
from dashboard import utils

st.set_page_config(page_title='Sales Analytics Dashboard', layout='wide')

@st.cache_data(ttl=600)
def load_data(limit=None):
    return load_sales_table(limit)


def sidebar_filters(df):
    years = sorted(df['order_date'].dt.year.astype(str).unique(), reverse=True)
    year = st.sidebar.selectbox('Year', options=['All']+years, index=0)
    months = list(range(1,13))
    month = st.sidebar.selectbox('Month', options=['All']+months, index=0)
    regions = ['All'] + sorted(df['region'].unique().tolist())
    region = st.sidebar.selectbox('Region', options=regions, index=0)
    categories = ['All'] + sorted(df['category'].unique().tolist())
    category = st.sidebar.selectbox('Category', options=categories, index=0)
    return year, month, region, category


def apply_filters(df, year, month, region, category):
    df2 = df.copy()
    if year != 'All':
        df2 = df2[df2['order_date'].dt.year == int(year)]
    if month != 'All':
        df2 = df2[df2['order_date'].dt.month == int(month)]
    if region != 'All':
        df2 = df2[df2['region'] == region]
    if category != 'All':
        df2 = df2[df2['category'] == category]
    return df2


def main():
    st.title('Sales Analytics Dashboard')
    # If the SQLite DB doesn't exist, generate the dataset and build the DB.
    db_full = os.path.join(ROOT, 'sql', 'sales_data.db')
    if not os.path.exists(db_full):
        with st.spinner('Generating synthetic dataset and building database (this may take a minute)...'):
            cwd = os.getcwd()
            os.chdir(ROOT)
            try:
                import data.generate_data as gen
                import data.clean_data as clean
                gen.main(rows=10000, out_csv='data/sales_data.csv')
                clean.clean()
            finally:
                os.chdir(cwd)
        st.success('Dataset generated and database created.')

    df = load_data()

    year, month, region, category = sidebar_filters(df)
    df_filtered = apply_filters(df, year, month, region, category)

    # KPI cards
    kpis = utils.kpi_metrics(df_filtered)
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric('Total Revenue', f"${kpis['total_revenue']:,.2f}")
    c2.metric('Total Orders', f"{kpis['total_orders']:,.0f}")
    c3.metric('Average Order Value', f"${kpis['aov']:,.2f}")
    c4.metric('Total Profit', f"${kpis['total_profit']:,.2f}")
    c5.metric('Profit Margin', f"{kpis['profit_margin']*100:.2f}%")

    # Charts
    st.subheader('Trends and Breakdowns')
    left, right = st.columns((2,1))
    with left:
        st.plotly_chart(utils.monthly_sales(df_filtered), use_container_width=True)
        # Year-over-Year growth
        try:
            yoy_fig, yoy_table = utils.yoy_growth(df_filtered)
            st.plotly_chart(yoy_fig, use_container_width=True)
        except Exception:
            st.info('YoY growth not available for current selection')
        st.plotly_chart(utils.sales_by_category(df_filtered), use_container_width=True)
    with right:
        st.plotly_chart(utils.sales_by_region(df_filtered), use_container_width=True)
        st.plotly_chart(utils.top_products(df_filtered), use_container_width=True)

    st.subheader('Customers and Profit Analysis')
    st.plotly_chart(utils.top_customers(df_filtered), use_container_width=True)

    st.subheader('Customer Segmentation (RFM)')
    try:
        rfm_fig, rfm_table = utils.rfm_segmentation(df_filtered)
        st.plotly_chart(rfm_fig, use_container_width=True)
        with st.expander('RFM table (sample)'):
            st.dataframe(rfm_table.sort_values('monetary', ascending=False).head(50))
    except Exception:
        st.info('RFM segmentation not available for current selection')

    st.subheader('Business Insights')
    insights = []
    try:
        top_cat = df_filtered.groupby('category')['revenue'].sum().idxmax()
        insights.append(f"Top category by revenue: {top_cat}.")
    except Exception:
        insights.append('Top category: N/A')
    try:
        top_reg = df_filtered.groupby('region')['revenue'].sum().idxmax()
        insights.append(f"Top region by revenue: {top_reg}.")
    except Exception:
        insights.append('Top region: N/A')
    try:
        total_rev = df_filtered['revenue'].sum()
        total_profit = df_filtered['profit'].sum()
        pm = (total_profit/total_rev) if total_rev!=0 else 0
        insights.append(f"Profit margin: {pm*100:.2f}%.")
    except Exception:
        insights.append('Profit margin: N/A')
    try:
        if 'yoy_table' in locals() and 'yoy_growth' in yoy_table.columns:
            last = yoy_table.dropna(subset=['yoy_growth']).iloc[-1]
            insights.append(f"Most recent YoY growth: {last['yoy_growth']*100:.2f}% for {int(last['year'])}.")
    except Exception:
        pass

    for i in insights:
        st.write(f"- {i}")

if __name__ == '__main__':
    main()
