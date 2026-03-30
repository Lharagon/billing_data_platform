from fastapi import FastAPI
import duckdb
import os
from pydantic import BaseModel

app = FastAPI()
DB = "dbt/data/warehouse.duckdb"

@app.get("/summary")
def summary():
    con = duckdb.connect(DB)
    df = con.execute("select dt, sum(total_amount) as total_amount, sum(event_count) as event_count from fct_billing group by dt order by dt desc limit 10").fetchdf()
    con.close()
    return {"rows": df.to_dict(orient="records")}

class PredictRequest(BaseModel):
    customer_id: str
