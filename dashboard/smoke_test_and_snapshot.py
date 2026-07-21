"""Smoke test dashboard components and produce a dashboard preview PNG.
Saves `images/dashboard-preview.png`.
"""
from pathlib import Path
import os
import sys

# Ensure repository root is on sys.path so absolute imports work when this
# script is executed directly (e.g., during CI or by users).
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from dashboard.data_loader import load_sales_table
from dashboard import utils
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import seaborn as sns
import os

OUT = Path('images/dashboard-preview.png')
TMP_DIR = Path('images/.tmp')
TMP_DIR.mkdir(parents=True, exist_ok=True)

def save_matplotlib(fig, name):
    path = TMP_DIR / f"{name}.png"
    fig.savefig(path, bbox_inches='tight')
    plt.close(fig)
    return path

def build_snapshot():
    df = load_sales_table()
    kpis = utils.kpi_metrics(df)

    # Monthly sales (line)
    dfm = df.copy()
    dfm['year_month'] = dfm['order_date'].dt.to_period('M').astype(str)
    monthly = dfm.groupby('year_month')['revenue'].sum().reset_index()
    fig1, ax1 = plt.subplots(figsize=(8,4))
    sns.lineplot(data=monthly, x='year_month', y='revenue', marker='o', ax=ax1)
    ax1.set_title('Monthly Sales Trend')
    ax1.set_xlabel('Month')
    ax1.set_ylabel('Revenue')
    plt.xticks(rotation=45)
    p1 = save_matplotlib(fig1, 'monthly')

    # Sales by category
    cat = df.groupby('category')['revenue'].sum().sort_values(ascending=False).reset_index()
    fig2, ax2 = plt.subplots(figsize=(4,3))
    sns.barplot(data=cat, x='revenue', y='category', ax=ax2)
    ax2.set_title('Sales by Category')
    p2 = save_matplotlib(fig2, 'by_category')

    # Sales by region
    reg = df.groupby('region')['revenue'].sum().sort_values(ascending=False).reset_index()
    fig3, ax3 = plt.subplots(figsize=(4,3))
    sns.barplot(data=reg, x='revenue', y='region', ax=ax3)
    ax3.set_title('Sales by Region')
    p3 = save_matplotlib(fig3, 'by_region')

    # Top products
    tp = df.groupby('product_name')['revenue'].sum().sort_values(ascending=False).head(10).reset_index()
    fig4, ax4 = plt.subplots(figsize=(6,3))
    sns.barplot(data=tp, x='revenue', y='product_name', ax=ax4)
    ax4.set_title('Top 10 Products')
    p4 = save_matplotlib(fig4, 'top_products')

    # Top customers
    tc = df.groupby('customer_name')['revenue'].sum().sort_values(ascending=False).head(10).reset_index()
    fig5, ax5 = plt.subplots(figsize=(6,3))
    sns.barplot(data=tc, x='revenue', y='customer_name', ax=ax5)
    ax5.set_title('Top Customers')
    p5 = save_matplotlib(fig5, 'top_customers')

    # Year-over-Year growth
    try:
        yoy_fig, yoy_table = utils.yoy_growth(df)
        # prepare matplotlib plot
        fig6, ax6 = plt.subplots(figsize=(4,3))
        sns.barplot(data=yoy_table.dropna(subset=['yoy_growth']), x='year', y='yoy_growth', ax=ax6)
        ax6.set_title('YoY Growth')
        ax6.set_ylabel('Growth')
        p6 = save_matplotlib(fig6, 'yoy_growth')
    except Exception:
        p6 = None

    # RFM segmentation
    try:
        rfm_fig, rfm_table = utils.rfm_segmentation(df)
        seg_counts = rfm_table['segment'].value_counts().reset_index()
        seg_counts.columns = ['segment','count']
        fig7, ax7 = plt.subplots(figsize=(4,3))
        sns.barplot(data=seg_counts, x='segment', y='count', ax=ax7)
        ax7.set_title('Customer Segments')
        p7 = save_matplotlib(fig7, 'rfm_segments')
    except Exception:
        p7 = None

    # Compose image
    widths = 1200
    height = 900
    canvas = Image.new('RGB', (widths, height), 'white')
    draw = ImageDraw.Draw(canvas)
    try:
        font = ImageFont.truetype('DejaVuSans-Bold.ttf', 28)
        small = ImageFont.truetype('DejaVuSans.ttf', 16)
    except Exception:
        font = ImageFont.load_default()
        small = ImageFont.load_default()
    draw.text((20,10), 'Sales Analytics Dashboard — Preview', fill='black', font=font)

    kpi_texts = [
        f"Total Revenue: ${kpis['total_revenue']:,.2f}",
        f"Total Orders: {kpis['total_orders']:,}",
        f"Avg Order Value: ${kpis['aov']:,.2f}",
        f"Total Profit: ${kpis['total_profit']:,.2f}",
        f"Profit Margin: {kpis['profit_margin']*100:.2f}%",
    ]
    x = 20
    y = 60
    for t in kpi_texts:
        draw.text((x,y), t, fill='black', font=small)
        x += 230

    img_monthly = Image.open(p1).resize((760,420))
    canvas.paste(img_monthly, (20,120))
    img_cat = Image.open(p2).resize((360,200))
    canvas.paste(img_cat, (800,120))
    img_region = Image.open(p3).resize((360,200))
    canvas.paste(img_region, (800,340))
    img_top_products = Image.open(p4).resize((560,240))
    canvas.paste(img_top_products, (20,560))
    # place top customers and RFM/YOY if available
    if p7:
        img_rfm = Image.open(p7).resize((360,200))
        canvas.paste(img_rfm, (800,560))
    if p6:
        img_yoy = Image.open(p6).resize((360,200))
        canvas.paste(img_yoy, (800,380))
    img_top_customers = Image.open(p5).resize((560,240))
    canvas.paste(img_top_customers, (620,560))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(OUT)
    # cleanup
    for p in TMP_DIR.iterdir():
        p.unlink()
    TMP_DIR.rmdir()
    print(f"Saved dashboard preview -> {OUT}")

if __name__ == '__main__':
    build_snapshot()
