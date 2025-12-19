import pandas as pd
import sqlite3
from pathlib import Path

DB_PATH = "data/Presentation/BIG_TABLE.db"

SOURCE_PATHS = {
    "japan": "source/japan_store",
    "myanmar": "source/myanmar_store"
}

conn = sqlite3.connect(DB_PATH)

for country, path in SOURCE_PATHS.items():
    for csv_file in Path(path).glob("*.csv"):
        table_name = f"stg_{country}_{csv_file.stem}"
        df = pd.read_csv(csv_file)
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        print(f"Loaded {csv_file.name} → {table_name}")

conn.close()
