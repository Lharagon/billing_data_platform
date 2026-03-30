import streamlit as st
import duckdb
import pandas as pd

DB = "data/warehouse.duckdb"

st.title("Billing & Product Analytics — Demo")
con = duckdb.connect(DB)

st.header("Latest daily billing")
df = con.execute("select dt, total_amount, event_count from fct_billing order by dt desc limit 30").fetchdf()
st.line_chart(df.set_index('dt')['total_amount'])

st.header("Product breakdown (last 30 days)")
prod = con.execute("select product_id, sum(total_amount) as revenue from fct_billing group by product_id").fetchdf()
st.table(prod)

st.header("Predict billing risk")
cust = st.text_input("Customer ID", "")
if st.button("Predict"):
    import requests
    resp = requests.post("http://localhost:8000/predict", json={"customer_id": cust})
    st.write(resp.json())

con.close()