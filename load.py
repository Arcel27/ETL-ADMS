import pandas as pd
import sqlite3
from sqlalchemy import create_engine

# ---------------------------------------------------------
# 1. EXTRACT: Connect to your local SQLite database
# ---------------------------------------------------------
LOCAL_DB_PATH = "data/Presentation/BIG_TABLE.db"
sqlite_conn = sqlite3.connect(LOCAL_DB_PATH)

# Read the tables from your local file
jp = pd.read_sql("SELECT * FROM trf_japan_sales", sqlite_conn)
mm = pd.read_sql("SELECT * FROM trf_myanmar_sales", sqlite_conn)

# Close the local connection since we have the data in memory now
sqlite_conn.close()

# ---------------------------------------------------------
# 2. TRANSFORM: Combine the data
# ---------------------------------------------------------
final_df = pd.concat([jp, mm], ignore_index=True)

# ---------------------------------------------------------
# 3. LOAD: Connect to the Render cloud database
# ---------------------------------------------------------
RENDER_DB_URI = "postgresql://db_nako_user:3halkU77mrx0Gaw8HxpVqoDGDDNSDCpc@dpg-d7ngs4vlk1mc73d4p9m0-a.singapore-postgres.render.com/db_nako"
render_engine = create_engine(RENDER_DB_URI)

# Push the combined data up to the cloud
final_df.to_sql(
    "final_consolidated_sales",
    render_engine,
    if_exists="replace",
    index=False
)

print("ETL process completed successfully! Data extracted from SQLite and loaded to Render.")