"""
sync_to_elastic.py  —  Run this during the demo.

Pipeline:
    products.json  →  PostgreSQL  →  Elasticsearch

Reads from the locally saved JSON (no internet needed).
Then loads into PostgreSQL and indexes into Elasticsearch.

Usage:
    python sync_to_elastic.py
"""

import json
import psycopg2
from psycopg2.extras import execute_batch
from elasticsearch import Elasticsearch, helpers

# ── Config (matches docker-compose.yml) ─────────────────────────────────────
PG_CONFIG = {
    "host":     "localhost",
    "port":     5432,
    "dbname":   "shopdb",
    "user":     "admin",
    "password": "secret",
}
ES_HOST   = "http://localhost:9200"
ES_INDEX  = "products"
DATA_FILE = "products.json"

# ── Elasticsearch mapping ────────────────────────────────────────────────────
INDEX_MAPPING = {
    "mappings": {
        "properties": {
            "id":          {"type": "integer"},
            "title":       {"type": "text",    "analyzer": "english"},
            "description": {"type": "text",    "analyzer": "english"},
            "price":       {"type": "float"},
            "category":    {"type": "keyword"},
            "rating":      {"type": "float"},
        }
    }
}


def load_json():
    with open(DATA_FILE, encoding="utf-8") as f:
        products = json.load(f)
    print(f"  Loaded {len(products)} products from {DATA_FILE}")
    return products


def load_postgres(products):
    conn = psycopg2.connect(**PG_CONFIG)
    cur  = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS products")
    cur.execute("""
        CREATE TABLE products (
            id          INTEGER PRIMARY KEY,
            title       VARCHAR(300)  NOT NULL,
            description TEXT          NOT NULL,
            price       NUMERIC(10,2) NOT NULL,
            category    VARCHAR(100)  NOT NULL,
            rating      NUMERIC(3,1)  DEFAULT 0
        )
    """)

    rows = [(p["id"], p["title"], p["description"],
             p["price"], p["category"], p["rating"]) for p in products]

    execute_batch(cur, """
        INSERT INTO products (id, title, description, price, category, rating)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, rows)

    conn.commit()
    cur.close()
    conn.close()
    print(f"  Inserted {len(rows)} rows into PostgreSQL")


def load_elasticsearch(products):
    es = Elasticsearch(ES_HOST)

    if es.indices.exists(index=ES_INDEX):
        es.indices.delete(index=ES_INDEX)
    es.indices.create(index=ES_INDEX, body=INDEX_MAPPING)

    actions = [
        {"_index": ES_INDEX, "_id": p["id"], "_source": p}
        for p in products
    ]
    ok, errors = helpers.bulk(es, actions)
    print(f"  Indexed {ok} documents into Elasticsearch ({len(errors)} errors)")
    return es


def search_demo(es, query):
    result = es.search(index=ES_INDEX, body={
        "query": {
            "multi_match": {
                "query":  query,
                "fields": ["title^2", "description", "category"],
            }
        },
        "size": 3,
    })
    hits = result["hits"]["hits"]
    print(f"\n  Search: '{query}'  →  {len(hits)} result(s)")
    for hit in hits:
        src   = hit["_source"]
        score = round(hit["_score"], 2)
        print(f"    [{score}]  {src['title'][:55]}  —  ${src['price']}")


# ── Main ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n=== Pipeline: products.json → PostgreSQL → Elasticsearch ===\n")

    print("[1/3] Reading local data...")
    products = load_json()

    print("[2/3] Loading into PostgreSQL...")
    load_postgres(products)

    print("[3/3] Indexing into Elasticsearch...")
    es = load_elasticsearch(products)

    print("\n--- Demo searches ---")
    search_demo(es, "wireless")
    search_demo(es, "men's clothing")
    search_demo(es, "gold ring")

    print("\n=== Done! ===")
    print("  pgAdmin  →  http://localhost:5050")
    print("  ES API   →  http://localhost:9200/products/_search?q=jacket&pretty")
