import os

print(os.getcwd())
print(os.listdir("data"))

import sqlite3
import pandas as pd

conn = sqlite3.connect("retail_etl.db")
DATA_PATH = "data/"


# JAPAN
japan_items = pd.read_csv(DATA_PATH + "japan_items.csv")
japan_sales = pd.read_csv(DATA_PATH + "sales_data.csv")
japan_customers = pd.read_csv(DATA_PATH + "japan_Customers.csv")
japan_branch = pd.read_csv(DATA_PATH + "japan_branch.csv")

japan_items.to_sql("stg_japan_items", conn, if_exists="replace", index=False)
japan_sales.to_sql("stg_japan_sales", conn, if_exists="replace", index=False)
japan_customers.to_sql("stg_japan_customers", conn, if_exists="replace", index=False)
japan_branch.to_sql("stg_japan_branch", conn, if_exists="replace", index=False)

# MYANMAR
myanmar_items = pd.read_csv(DATA_PATH + "myanmar_items.csv")
myanmar_sales = pd.read_csv(DATA_PATH + "myanmar_sales.csv")
myanmar_customers = pd.read_csv(DATA_PATH + "myanmar_customers.csv")
myanmar_branch = pd.read_csv(DATA_PATH + "myanmar_branch.csv")

myanmar_items.to_sql("stg_myanmar_items", conn, if_exists="replace", index=False)
myanmar_sales.to_sql("stg_myanmar_sales", conn, if_exists="replace", index=False)
myanmar_customers.to_sql("stg_myanmar_customers", conn, if_exists="replace", index=False)
myanmar_branch.to_sql("stg_myanmar_branch", conn, if_exists="replace", index=False)


JPY_TO_USD = 1 / 150

japan_items["price_usd"] = japan_items["price"] * JPY_TO_USD
japan_items["country"] = "Japan"
japan_items.dropna(inplace=True)

myanmar_items["price_usd"] = myanmar_items["price"]
myanmar_items["country"] = "Myanmar"
myanmar_items.dropna(inplace=True)

japan_items.to_sql("trf_japan_items", conn, if_exists="replace", index=False)
myanmar_items.to_sql("trf_myanmar_items", conn, if_exists="replace", index=False)


query = """
DROP TABLE IF EXISTS prs_consolidated_sales;

CREATE TABLE prs_consolidated_sales AS
SELECT
    s.invoice_id,
    'Japan' AS country,
    b.city AS branch_city,
    c.name AS customer_name,
    i.product_name,
    i.category,
    i.price_usd,
    s.quantity,
    (i.price_usd * s.quantity) AS total_sales_usd,
    s.date,
    s.payment,
    s.rating
FROM stg_japan_sales s
JOIN trf_japan_items i ON s.product_id = i.id
JOIN stg_japan_customers c ON s.customer_id = c.id
JOIN stg_japan_branch b ON s.branch_id = b.id

UNION ALL

SELECT
    s.invoice_id,
    'Myanmar' AS country,
    b.city AS branch_city,
    c.name AS customer_name,
    i.product_name,
    i.category,
    i.price_usd,
    s.quantity,
    (i.price_usd * s.quantity) AS total_sales_usd,
    s.date,
    s.payment,
    s.rating
FROM stg_myanmar_sales s
JOIN trf_myanmar_items i ON s.product_id = i.id
JOIN stg_myanmar_customers c ON s.customer_id = c.id
JOIN stg_myanmar_branch b ON s.branch_id = b.id;
"""

conn.executescript(query)


df = pd.read_sql("SELECT * FROM prs_consolidated_sales", conn)

print("\nInsight 1: Avg Revenue per Transaction")
print(df.groupby("country")["total_sales_usd"].mean())

print("\nInsight 2: Top Categories")
print(df.groupby("category")["total_sales_usd"].sum().sort_values(ascending=False))

print("\nInsight 3: Avg Quantity per Transaction")
print(df.groupby("country")["quantity"].mean())

print("\nInsight 4: Rating vs Revenue Correlation")
print(df[["rating", "total_sales_usd"]].corr())

print("\nInsight 5: Revenue by Hour")
df["hour"] = pd.to_datetime(df["date"]).dt.hour
print(df.groupby("hour")["total_sales_usd"].mean())


