import pandas as pd
import plotly.express as px


def kpi_metrics(df):
    total_revenue = df['revenue'].sum()
    total_orders = df['order_id'].nunique()
    aov = df['order_value'].mean()
    total_profit = df['profit'].sum()
    profit_margin = total_profit/total_revenue if total_revenue!=0 else 0
    return dict(total_revenue=total_revenue, total_orders=total_orders, aov=aov, total_profit=total_profit, profit_margin=profit_margin)


def monthly_sales(df):
    df2 = df.copy()
    df2['year_month'] = df2['order_date'].dt.to_period('M').astype(str)
    out = df2.groupby('year_month')['revenue'].sum().reset_index()
    fig = px.line(out, x='year_month', y='revenue', title='Monthly Sales Trend')
    fig.update_layout(xaxis_title='Month', yaxis_title='Revenue')
    return fig


def sales_by_category(df):
    out = df.groupby('category')['revenue'].sum().reset_index().sort_values('revenue', ascending=False)
    fig = px.bar(out, x='category', y='revenue', title='Sales by Category')
    return fig


def sales_by_region(df):
    out = df.groupby('region')['revenue'].sum().reset_index().sort_values('revenue', ascending=False)
    fig = px.bar(out, x='region', y='revenue', title='Sales by Region')
    return fig


def top_products(df, n=10):
    out = df.groupby(['product_id','product_name'])['revenue'].sum().reset_index().sort_values('revenue', ascending=False).head(n)
    fig = px.bar(out, x='product_name', y='revenue', title=f'Top {n} Products')
    return fig


def top_customers(df, n=10):
    out = df.groupby(['customer_id','customer_name'])['revenue'].sum().reset_index().sort_values('revenue', ascending=False).head(n)
    fig = px.bar(out, x='customer_name', y='revenue', title=f'Top {n} Customers')
    return fig


def yoy_growth(df):
    # Year over Year growth by year
    df2 = df.copy()
    df2['year'] = df2['order_date'].dt.year
    out = df2.groupby('year')['revenue'].sum().reset_index().sort_values('year')
    out['prev_revenue'] = out['revenue'].shift(1)
    out['yoy_growth'] = (out['revenue'] - out['prev_revenue']) / out['prev_revenue']
    fig = px.bar(out, x='year', y='yoy_growth', title='Year-over-Year Revenue Growth', labels={'yoy_growth':'YoY Growth'})
    fig.update_layout(yaxis_tickformat='.0%')
    return fig, out


def rfm_segmentation(df, reference_date=None):
    # Recency, Frequency, Monetary per customer
    df2 = df.copy()
    if reference_date is None:
        reference_date = df2['order_date'].max() + pd.Timedelta(days=1)
    agg = df2.groupby(['customer_id','customer_name']).agg(
        recency_days=('order_date', lambda x: (reference_date - x.max()).days),
        frequency=('order_id', 'nunique'),
        monetary=('revenue', 'sum')
    ).reset_index()

    # Score 1-5 using quantiles (5 is best for monetary & frequency, 1 is most recent)
    agg['r_score'] = pd.qcut(agg['recency_days'], 5, labels=[5,4,3,2,1]).astype(int)
    agg['f_score'] = pd.qcut(agg['frequency'].rank(method='first'), 5, labels=[1,2,3,4,5]).astype(int)
    agg['m_score'] = pd.qcut(agg['monetary'], 5, labels=[1,2,3,4,5]).astype(int)
    agg['rfm_score'] = agg['r_score'].astype(str) + agg['f_score'].astype(str) + agg['m_score'].astype(str)
    agg['rfm_sum'] = agg[['r_score','f_score','m_score']].sum(axis=1)

    # Simple segmentation based on rfm_sum
    def seg_label(x):
        if x >= 13:
            return 'Champions'
        if x >= 10:
            return 'Loyal'
        if x >= 7:
            return 'Potential'
        if x >= 4:
            return 'Needs Attention'
        return 'At Risk'

    agg['segment'] = agg['rfm_sum'].apply(seg_label)

    # Chart: segment counts
    seg_counts = agg['segment'].value_counts().reset_index()
    seg_counts.columns = ['segment','count']
    fig = px.bar(seg_counts, x='segment', y='count', title='Customer Segments (RFM)')
    return fig, agg
