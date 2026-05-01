"""
fetch_data.py  —  Run this ONCE at home before the demo.

Fetches product data from Fake Store API and saves it to products.json.
During the demo, sync_to_elastic.py reads from that local file — no internet needed.

Usage:
    python fetch_data.py
"""

import json
import requests

API_URL = "https://fakestoreapi.com/products"
OUTPUT  = "products.json"

print(f"Fetching from {API_URL} ...")
resp = requests.get(API_URL, timeout=10)
resp.raise_for_status()

products = resp.json()

# Keep only the fields we care about
cleaned = [
    {
        "id":          p["id"],
        "title":       p["title"],
        "description": p["description"],
        "price":       p["price"],
        "category":    p["category"],
        "rating":      p.get("rating", {}).get("rate", 0.0),
    }
    for p in products
]

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(cleaned, f, indent=2, ensure_ascii=False)

print(f"Saved {len(cleaned)} products to {OUTPUT}")
print("You can now run sync_to_elastic.py offline during the demo.")
