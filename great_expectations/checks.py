import duckdb
def check_not_null(table, col):
    con = duckdb.connect("data/warehouse.duckdb")
    res = con.execute(f"select count(*) as cnt from {table} where {col} is null").fetchdf()
    con.close()
    return int(res['cnt'].iloc[0]) == 0

if __name__ == "__main__":
    print("stg_billing_events.amount not null:", check_not_null("stg_billing_events", "amount"))