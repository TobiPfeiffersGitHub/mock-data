import pandas as pd
import json
import random
from pathlib import Path
from datetime import datetime, timedelta

# --- Config ---
BASE_PATH = Path(__file__).parent
DATA_PATH = BASE_PATH / "data"
OUTPUT_PATH = BASE_PATH / "output"

# Ensure output path exists
OUTPUT_PATH.mkdir(exist_ok=True)

# --- Load Parquet Data ---
store_df = pd.read_parquet(DATA_PATH / "store.parquet")
product_df = pd.read_parquet(DATA_PATH / "product.parquet")

# --- Select SKUs ---
store_skus = store_df.sample(2, random_state=42)["store_sk"].tolist()
product_skus = product_df.sample(10, random_state=42)["product_sk"].tolist()

# --- Generate Availability JSON ---
availability_data = {}

for store in store_skus:
    availability_data[store] = {}
    for product in product_skus:
        quantity = random.randint(0, 100)
        days_ahead = random.randint(0, 7)
        atp_date = (datetime.now() + timedelta(days=days_ahead)).strftime("%Y-%m-%d")
        availability_data[store][product] = {
            "ATP": {
                "MESSAGES": [],
                "AVAILABILITY": [
                    {
                        "ATP_DATE": atp_date,
                        "QUANTITY": quantity
                    }
                ]
            }
        }

with open(OUTPUT_PATH / "mock_availability.json", "w") as f:
    json.dump(availability_data, f, indent=2)

# --- Generate Product Info JSON ---
def generate_allergens():
    """Generate a list of allergens for a product"""
    common_allergens = [
        {"name": "Milk", "contains": True},
        {"name": "Eggs", "contains": True},
        {"name": "Fish", "contains": True},
        {"name": "Crustacean shellfish", "contains": True},
        {"name": "Tree nuts", "contains": True},
        {"name": "Peanuts", "contains": True},
        {"name": "Wheat", "contains": True},
        {"name": "Soybeans", "contains": True},
        {"name": "Sesame", "contains": True},
        {"name": "Celery", "contains": True},
        {"name": "Mustard", "contains": True},
        {"name": "Sulphur dioxide and sulphites", "contains": True},
        {"name": "Lupin", "contains": True},
        {"name": "Molluscs", "contains": True}
    ]
    
    # 30% chance of no allergens
    if random.random() < 0.3:
        return []
    
    # Otherwise, randomly select 1-4 allergens
    num_allergens = random.randint(1, 4)
    return random.sample(common_allergens, num_allergens)

def generate_product_info(sku):
    return {
        "data": {
            "sku": sku,
            "name": f"Mock Product {sku[-4:]}",
            "brandName": "GENERIC",
            "description": "Lorem ipsum dolor sit amet.",
            "metaRobots": "index, follow",
            "notForSale": False,
            "quantityMin": 1,
            "quantityMax": 99,
            "quantityUnit": "ea",
            "sellingSize": "1 Unit",
            "storageInstructions": "Store in a cool dry place.",
            "ingredients": "Ingredient A, Ingredient B",
            "stockInformationAvailable": True,
            "price": {
                "amount": random.randint(100, 999),
                "currencyCode": "GBP",
                "currencySymbol": "£"
            },
            "categories": [
                {"id": "1234", "name": "Mock Category", "urlSlugText": "mock-category"}
            ],
            "assets": [],
            "nutritionalClaims": [],
            "allergens": generate_allergens()
        }
    }

product_data = {sku: generate_product_info(sku) for sku in product_skus}

with open(OUTPUT_PATH / "mock_products.json", "w") as f:
    json.dump(product_data, f, indent=2)