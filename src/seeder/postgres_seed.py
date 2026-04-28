import uuid
import random
import json
from datetime import datetime, timezone
import psycopg2
from psycopg2.extras import execute_values

# Настройки подключения к БД
DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432
}

CATEGORIES =[
    {"id": "019dce61-42de-71b9-a5b8-272287ddc3df", "name": "Смартфоны"},
    {"id": "019dce61-843a-74fa-a8dc-e751e3ed9eaa", "name": "Ноутбуки"},
    {"id": "019dce61-bb38-736c-bd20-2f599ddf1bad", "name": "Бытовая техника"},
    {"id": "019dce61-ea12-703c-95ea-24d098bec0b5", "name": "Одежда"},
    {"id": "019dce62-20ae-740e-a0af-de71d4707ea8", "name": "Спорттовары"}
]

ATTRIBUTES_POOL = {
    "Смартфоны": {"color": ("keyword",["black", "white", "silver", "blue", "red", "titanium"]), "memory": ("keyword",["64gb", "128gb", "256gb", "512gb", "1tb"]), "ram": ("number", [4, 6, 8, 12, 16])},
    "Ноутбуки": {"color": ("keyword", ["space gray", "silver", "black"]), "cpu": ("keyword",["Intel Core i5", "Intel Core i7", "AMD Ryzen 5", "AMD Ryzen 7"])},
    "Бытовая техника": {"type": ("keyword",["Холодильник", "Микроволновка"]), "power_w": ("number",[800, 1000, 1500, 2000, 2500])},
    "Одежда": {"size": ("keyword",["XS", "S", "M", "L", "XL", "XXL"]), "color": ("keyword",["black", "white", "red", "blue"])},
    "Спорттовары": {"sport_type": ("keyword",["Футбол", "Баскетбол", "Фитнес"]), "weight_kg": ("number",[0.5, 1, 2, 5, 10, 20])}
}

BRANDS =["Apple", "Samsung", "Xiaomi", "Bosch", "LG", "Nike", "Adidas", "Puma", "Asus", "Lenovo"]
units = {"memory": "GB", "ram": "GB", "power_w": "W", "weight_kg": "kg"}

def generate_pg_attributes(category_name):
    """Генерирует плоский словарь для JSONB"""
    attributes_dict = {}
    pool = ATTRIBUTES_POOL.get(category_name, {})
    if not pool: return attributes_dict

    num_attributes_to_pick = random.randint(2, len(pool))
    chosen_keys = random.sample(list(pool.keys()), num_attributes_to_pick)

    for key in chosen_keys:
        attr_type, values = pool[key]
        chosen_value = random.choice(values)

        if attr_type == "number":
            unit = units.get(key, "")
            attributes_dict[key] = f"{chosen_value} {unit}".strip()
        else:
            attributes_dict[key] = chosen_value

    return attributes_dict

def generate_pg_records(num_docs=100000):
    """Генератор кортежей для массовой вставки в Postgres"""
    for _ in range(num_docs):
        category = random.choice(CATEGORIES)
        brand = random.choice(BRANDS)
        item_type = category["name"][:-1] if category["name"].endswith('ы') else category["name"]
        product_name = f"{item_type} {brand} {random.randint(100, 9999)}"

        attributes = generate_pg_attributes(category["name"])
        now = datetime.now(timezone.utc)

        yield (
            str(uuid.uuid4()),                # id
            product_name,                     # name
            category["id"],                   # category_id
            random.randint(100000, 20000000), # price_cents
            f"Отличный {product_name}",       # description
            json.dumps(attributes),           # attributes (jsonb)
            now,                              # created_at
            now,                              # updated_at
            brand                             # brand
        )

if __name__ == "__main__":
    print("Подключение к PostgreSQL...")
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Для теста генерируем сразу 100 000 товаров, чтобы было с чем работать
    TOTAL_RECORDS = 100000
    BATCH_SIZE = 5000

    insert_query = """
        INSERT INTO products (id, name, category_id, price_cents, description, attributes, created_at, updated_at, brand)
        VALUES %s
    """

    print(f"Генерация и загрузка {TOTAL_RECORDS} товаров в PostgreSQL...")

    records =[]
    inserted = 0
    for record in generate_pg_records(TOTAL_RECORDS):
        records.append(record)
        if len(records) >= BATCH_SIZE:
            execute_values(cursor, insert_query, records)
            conn.commit()
            inserted += len(records)
            print(f"Загружено {inserted} / {TOTAL_RECORDS}...")
            records = []

    # Дозагружаем остатки, если они есть
    if records:
        execute_values(cursor, insert_query, records)
        conn.commit()
        inserted += len(records)
        print(f"Финальная загрузка: {inserted} / {TOTAL_RECORDS}...")

    cursor.close()
    conn.close()
    print("Загрузка в PostgreSQL завершена успешно.")
