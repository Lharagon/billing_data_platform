import argparse
import random
import uuid
import csv
from datetime import datetime, timedelta
import os

PRODUCTS = [
    {"product_id": "P-A", "category": "Analytics", "price": 99.0},
    {"product_id": "P-B", "category": "Billing", "price": 149.0},
    {"product_id": "P-C", "category": "Telehealth", "price": 49.0},
]

def random_date(start, end):
    return start + timedelta(
        seconds=random.randint(0, 
                               int((end - start).total_seconds())))

def generate_customers(n):
    customers = []
    for i in range(n):
        customers.append({
            "customer_id": f"CUST-{1000+i}",
            "first_name": f"Name{i}",
            "last_name": f"Surname{i}",
            "signup_date": (
                datetime.now() - timedelta(
                    days=random.randint(0, 1000))).strftime("%Y-%m-%d")
        })
    return customers

def generate_events(customers, n_events):
    events = []
    start = datetime.now() - timedelta(days=365)
    end = datetime.now()
    for _ in range(n_events):
        cust = random.choice(customers)
        product = random.choice(PRODUCTS)
        event_time = random_date(start, end)
        status = random.choices(
            ["paid", "pending", "failed"], weights=[0.7, 0.2, 0.1])[0]
        amount = product["price"] * random.choice([1, 1, 1, 2])
        events.append({
            "event_id": str(uuid.uuid4()),
            "customer_id": cust["customer_id"],
            "product_id": product["product_id"],
            "category": product["category"],
            "amount": amount,
            "status": status,
            "event_time": event_time.strftime("%Y-%m-%d %H:%M:%S")
        })
    return events

def save_csv(rows, path, fields):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

def main(args):
    customers = generate_customers(args.n_customers)
    events = generate_events(customers, args.n_events)
    save_csv(customers, os.path.join(args.output_dir, "customers.csv"),
             ["customer_id", "first_name", "last_name", "signup_date"])
    save_csv(events, os.path.join(args.output_dir, "billing_events.csv"),
             ["event_id", "customer_id", "product_id", 
              "category", "amount", "status", "event_time"])
    print(f"Saved customers and {len(events)} events to {args.output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_dir", default="data/raw")
    parser.add_argument("--n_customers", type=int, default=200)
    parser.add_argument("--n_events", type=int, default=2000)
    args = parser.parse_args()
    main(args)