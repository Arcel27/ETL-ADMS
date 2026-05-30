import pandas as pd
import sqlite3
from pathlib import Path
import os

# 1. Automatically create the Presentation folder if it doesn't exist
os.makedirs("data/Presentation", exist_ok=True)
DB_PATH = "data/Presentation/BIG_TABLE.db"

# 2. Fixed paths to match your VS Code folder structure!
SOURCE_PATHS = {
    "japan": "data/source/japan_store",
    "myanmar": "data/source/myanmar_store"
}

conn = sqlite3.connect(DB_PATH)

for country, path in SOURCE_PATHS.items():
    for csv_file in Path(path).glob("*.csv"):
        table_name = f"stg_{country}_{csv_file.stem}"
        df = pd.read_csv(csv_file)
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        print(f"Loaded {csv_file.name} → {table_name}")

conn.close()