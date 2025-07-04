import csv
import sys
import os
import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.db import SessionLocal
from app.models.product import Product, LocationEnum
from app.models.user import User
from app.models.order import Order
from app.core.security import get_password_hash

# Model registry: model name -> dict with model class, unique keys, and enum fields
MODEL_REGISTRY = {
    "product": {
        "model": Product,
        "unique_keys": ["title", "location", "id"],
        "enum_fields": {"location": LocationEnum, "id": int},
        "type_casts": {"price": float, "id": int, "title": str, "description": str, "location": LocationEnum}
    },
    "user": {
        "model": User,
        "unique_keys": ["id"],
        "enum_fields": {},
        "type_casts": {"id": int, "password": str, "username": str }
    },
  
    # Add more models here as needed
}

def convert_row(row, type_casts, enum_fields):
    new_row = {}
    for k, v in row.items():
        k = k.strip()  # Remove leading/trailing spaces from header
        if isinstance(v, str):
            v = v.strip()  # Remove leading/trailing spaces from value
        if k in enum_fields:
            new_row[k] = enum_fields[k](v)
        elif k in type_casts:
            new_row[k] = type_casts[k](v)
        else:
            new_row[k] = v
    # Set created_at and updated_at to now if missing or empty
    now = datetime.datetime.now()
    if not new_row.get('created_at'):
        new_row['created_at'] = now
    if not new_row.get('updated_at'):
        new_row['updated_at'] = now
    # deleted_at can remain None if not present
    return new_row

def import_csv(model_name, csv_path):
    if model_name not in MODEL_REGISTRY:
        print(f"Model '{model_name}' is not registered.")
        sys.exit(1)
    reg = MODEL_REGISTRY[model_name]
    Model = reg["model"]
    unique_keys = reg["unique_keys"]
    enum_fields = reg.get("enum_fields", {})
    type_casts = reg.get("type_casts", {})

    db = SessionLocal()
    added = 0
    updated = 0
    skipped = 0
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row = convert_row(row, type_casts, enum_fields)
            # Hash password for users
            if model_name == "user" and "password" in row:
                row["password"] = get_password_hash(row["password"])
            filter_kwargs = {k: row[k] for k in unique_keys}
            existing = db.query(Model).filter_by(**filter_kwargs).first()
            if existing:
                updated_flag = False
                for k, v in row.items():
                    if hasattr(existing, k) and getattr(existing, k) != v:
                        setattr(existing, k, v)
                        updated_flag = True
                if updated_flag:
                    updated += 1
                else:
                    skipped += 1
                continue
            obj = Model(**row)
            db.add(obj)
            added += 1
        db.commit()
    db.close()
    print(f'✅ {model_name.capitalize()} import complete. Added: {added}, Updated: {updated}, Skipped (no changes): {skipped}')

def main():
    if len(sys.argv) != 3:
        print('Usage: python import_data.py <model_type> <csv_path>')
        print('  model_type: product | user')
        sys.exit(1)
    model_type = sys.argv[1].lower()
    csv_path = sys.argv[2]
    if not os.path.exists(csv_path):
        print(f'CSV file not found: {csv_path}')
        sys.exit(1)
    import_csv(model_type, csv_path)

if __name__ == '__main__':
    main() 