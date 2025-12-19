import pandas as pd
import sqlite3

DB_PATH = "data/Presentation/BIG_TABLE.db"
conn = sqlite3.connect(DB_PATH)

jp = pd.read_sql("SELECT * FROM trf_japan_sales", conn)
mm = pd.read_sql("SELECT * FROM trf_myanmar_sales", conn)

final_df = pd.concat([jp, mm], ignore_index=True)

final_df.to_sql(
    "final_consolidated_sales",
    conn,
    if_exists="replace",
    index=False
)

conn.close()
