import pandas as pd
import sqlite3

DB_PATH = "data/Presentation/BIG_TABLE.db"
USD_TO_JPY = 150

conn = sqlite3.connect(DB_PATH)

# READ ACTUAL STAGING TABLES
jp_sales = pd.read_sql("SELECT * FROM stg_japan_sales_data", conn)
mm_sales = pd.read_sql("SELECT * FROM stg_myanmar_sales_data", conn)

# --- Data Cleaning ---
jp_sales.dropna(inplace=True)
mm_sales.dropna(inplace=True)

jp_sales["price"] = jp_sales["price"].astype(float)
mm_sales["price"] = mm_sales["price"].astype(float)

# --- Standardization ---
jp_sales["country"] = "Japan"
mm_sales["country"] = "Myanmar"

# Convert Myanmar USD → JPY
mm_sales["price_jpy"] = mm_sales["price"] * USD_TO_JPY
jp_sales["price_jpy"] = jp_sales["price"]

# Select common columns
cols = ["order_id", "item_id", "quantity", "price_jpy", "country"]

jp_clean = jp_sales[cols]
mm_clean = mm_sales[cols]

# Save transformed data
jp_clean.to_sql("trf_japan_sales", conn, if_exists="replace", index=False)
mm_clean.to_sql("trf_myanmar_sales", conn, if_exists="replace", index=False)

conn.close()
