import pandas as pd
import sqlite3

DB_PATH = "data/Presentation/BIG_TABLE.db"
USD_TO_JPY = 150

conn = sqlite3.connect(DB_PATH)

jp_sales = pd.read_sql("SELECT * FROM stg_japan_sales_data", conn)
mm_sales = pd.read_sql("SELECT * FROM stg_myanmar_sales_data", conn)
jp_items = pd.read_sql("SELECT * FROM stg_japan_japan_items", conn)
mm_items = pd.read_sql("SELECT * FROM stg_myanmar_myanmar_items", conn)

for df in [jp_sales, mm_sales, jp_items, mm_items]:
    df.columns = df.columns.str.replace("'", "", regex=False).str.strip().str.lower()

jp_sales.rename(columns={'invoice_id': 'order_id', 'product_id': 'item_id'}, inplace=True)
mm_sales.rename(columns={'invoice_id': 'order_id', 'product_id': 'item_id'}, inplace=True)

jp_items.rename(columns={'id': 'item_id'}, inplace=True)
mm_items.rename(columns={'id': 'item_id'}, inplace=True)

jp_merged = pd.merge(jp_sales, jp_items, on="item_id", how="left")
mm_merged = pd.merge(mm_sales, mm_items, on="item_id", how="left")

jp_merged.dropna(subset=['price'], inplace=True)
mm_merged.dropna(subset=['price'], inplace=True)

jp_merged["price"] = jp_merged["price"].astype(float)
mm_merged["price"] = mm_merged["price"].astype(float)

jp_merged["country"] = "Japan"
mm_merged["country"] = "Myanmar"

jp_merged["price_jpy"] = jp_merged["price"]
mm_merged["price_jpy"] = mm_merged["price"] * USD_TO_JPY

cols = ["order_id", "item_id", "quantity", "price_jpy", "country"]

jp_clean = jp_merged[cols]
mm_clean = mm_merged[cols]

jp_clean.to_sql("trf_japan_sales", conn, if_exists="replace", index=False)
mm_clean.to_sql("trf_myanmar_sales", conn, if_exists="replace", index=False)

conn.close()
print("Transformation successful! Ready for load.py.")