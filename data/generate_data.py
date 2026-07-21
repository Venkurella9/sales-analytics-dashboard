"""
Generate a realistic synthetic retail sales dataset and save to CSV.
Generates at least 100,000 rows by default.
"""
import argparse
from faker import Faker
import numpy as np
import pandas as pd
import random

fake = Faker()

PRODUCT_CATEGORIES = {
    'Electronics': ['Laptop', 'Smartphone', 'Headphones', 'Camera', 'TV'],
    'Home & Kitchen': ['Blender', 'Cookware', 'Vacuum', 'Lamp', 'Chair'],
    'Clothing': ['T-Shirt', 'Jeans', 'Jacket', 'Dress', 'Shoes'],
    'Sports': ['Bicycle', 'Tennis Racket', 'Running Shoes', 'Yoga Mat', 'Dumbbells'],
    'Beauty': ['Skincare', 'Perfume', 'Makeup', 'Shampoo', 'Conditioner']
}

REGIONS = ['North', 'South', 'East', 'West']
PAYMENT_METHODS = ['Credit Card', 'PayPal', 'Debit Card', 'Cash']



def generate_products(n_products=200):
    products = []
    pid = 1000
    for cat, items in PRODUCT_CATEGORIES.items():
        for item in items:
            for i in range(10):
                products.append({
                    'product_id': pid,
                    'category': cat,
                    'product_name': f"{item} {i+1}",
                    'unit_cost': round(random.uniform(5, 500), 2),
                    'unit_price': None
                })
                pid += 1
    # Set unit_price as cost * markup
    for p in products:
        markup = random.uniform(1.1, 2.5)
        p['unit_price'] = round(p['unit_cost'] * markup, 2)
    return pd.DataFrame(products)


def main(rows=100000, out_csv='data/sales_data.csv'):
    n = max(int(rows), 100000)
    products = generate_products()
    n_products = len(products)

    start = pd.to_datetime('2019-01-01')
    end = pd.to_datetime('2024-12-31')

    order_ids = np.arange(1, n+1)
    order_dates = pd.to_datetime(np.random.randint(int(start.value//10**9), int(end.value//10**9), n), unit='s')

    customer_ids = np.random.randint(1000, 5000, size=n)
    customer_names = [fake.name() for _ in range(n)]
    regions = np.random.choice(REGIONS, size=n, p=[0.25,0.25,0.25,0.25])
    payment_methods = np.random.choice(PAYMENT_METHODS, size=n, p=[0.5,0.2,0.2,0.1])

    product_idxs = np.random.randint(0, n_products, size=n)
    chosen = products.iloc[product_idxs].reset_index(drop=True)

    quantities = np.random.poisson(2, size=n) + 1
    discounts = np.round(np.random.choice([0.0, 0.05, 0.1, 0.15, 0.2], size=n, p=[0.6,0.15,0.15,0.06,0.04]),2)

    df = pd.DataFrame({
        'order_id': order_ids,
        'order_date': order_dates,
        'customer_id': customer_ids,
        'customer_name': customer_names,
        'region': regions,
        'payment_method': payment_methods,
        'product_id': chosen['product_id'],
        'product_name': chosen['product_name'],
        'category': chosen['category'],
        'unit_price': chosen['unit_price'],
        'unit_cost': chosen['unit_cost'],
        'quantity': quantities,
        'discount': discounts,
    })

    df['revenue'] = (df['unit_price'] * df['quantity'] * (1 - df['discount'])).round(2)
    df['cost'] = (df['unit_cost'] * df['quantity']).round(2)
    df['profit'] = (df['revenue'] - df['cost']).round(2)
    df['order_value'] = df['revenue']

    # Add geographic granularity
    df['country'] = 'USA'
    df['city'] = [fake.city() for _ in range(n)]

    df.to_csv(out_csv, index=False)
    print(f"Generated {len(df)} rows -> {out_csv}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--rows', type=int, default=100000)
    parser.add_argument('--out', type=str, default='data/sales_data.csv')
    args = parser.parse_args()
    main(rows=args.rows, out_csv=args.out)
