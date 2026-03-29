import pandas as pd
import duckdb
import os

RAW_DIR = "data/raw"
DUCK_DB = "data/warehouse.duckdb"

def load_csv_to_duckdb(table_name, csv_path):
    con = duckdb.connect(DUCK_DB)
    df = pd.read_csv(csv_path)
    con.execute((
        f"CREATE TABLE IF NOT EXISTS {table_name} "
        "AS SELECT * "
        f"FROM read_csv_auto('{csv_path}') "
    ))
    con.close()
    print(f"Loaded {csv_path} into {table_name}")

def main():
    os.makedirs("data", exist_ok=True)
    load_csv_to_duckdb("stg_customers", 
                       os.path.join(RAW_DIR, "customers.csv"))
    load_csv_to_duckdb("stg_billing_events", 
                       os.path.join(RAW_DIR, "billing_events.csv"))

if __name__ == "__main__":
    main()
