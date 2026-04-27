import uuid
import random
from datetime import datetime, timezone
from elasticsearch import Elasticsearch, helpers

# Подключение к Elastic (укажи свои данные, если они отличаются)
es = Elasticsearch("http://localhost:9200")
INDEX_NAME = "products"

CATEGORIES =[
    {"id": "019dce61-42de-71b9-a5b8-272287ddc3df", "name": "Смартфоны"},
    {"id": "019dce61-843a-74fa-a8dc-e751e3ed9eaa", "name": "Ноутбуки"},
    {"id": "019dce61-bb38-736c-bd20-2f599ddf1bad", "name": "Бытовая техника"},
    {"id": "019dce61-ea12-703c-95ea-24d098bec0b5", "name": "Одежда"},
    {"id": "019dce62-20ae-740e-a0af-de71d4707ea8", "name": "Спорттовары"}
]
# Базы данных возможных характеристик для разнородности
# Формат: "название_атрибута": (тип, [варианты_значений])
ATTRIBUTES_POOL = {
    "Смартфоны": {
        "color": ("keyword",["black", "white", "silver", "blue", "red", "titanium"]),
        "memory": ("keyword",["64gb", "128gb", "256gb", "512gb", "1tb"]),
        "ram": ("number", [4, 6, 8, 12, 16]),
        "screen_size": ("number",[5.8, 6.1, 6.5, 6.7, 6.9]),
        "camera_mp": ("number",[12, 48, 50, 108, 200]),
        "os": ("keyword", ["iOS", "Android"]),
        "5g_support": ("keyword", ["yes", "no"])
    },
    "Ноутбуки": {
        "color": ("keyword", ["space gray", "silver", "black"]),
        "cpu": ("keyword",["Intel Core i5", "Intel Core i7", "AMD Ryzen 5", "AMD Ryzen 7", "Apple M2", "Apple M3"]),
        "ram": ("number",[8, 16, 32, 64]),
        "storage_capacity": ("number",[256, 512, 1024, 2048]),
        "storage_type": ("keyword", ["SSD", "HDD"]),
        "screen_size": ("number",[13.3, 14.0, 15.6, 16.0, 17.3]),
        "weight_kg": ("number",[1.2, 1.5, 2.0, 2.5])
    },
    "Бытовая техника": {
        "type": ("keyword",["Холодильник", "Микроволновка", "Стиральная машина", "Пылесос", "Чайник"]),
        "power_w": ("number",[800, 1000, 1500, 2000, 2500]),
        "energy_class": ("keyword",["A", "A+", "A++", "A+++", "B"]),
        "color": ("keyword",["white", "black", "silver", "beige"]),
        "noise_level_db": ("number",[30, 40, 50, 60, 75]),
        "warranty_years": ("number",[1, 2, 3, 5])
    },
    "Одежда": {
        "type": ("keyword",["Футболка", "Джинсы", "Куртка", "Худи", "Кроссовки"]),
        "size": ("keyword", ["XS", "S", "M", "L", "XL", "XXL"]),
        "color": ("keyword",["black", "white", "red", "blue", "green", "yellow"]),
        "material": ("keyword",["cotton", "polyester", "wool", "denim", "leather"]),
        "gender": ("keyword", ["male", "female", "unisex"]),
        "season": ("keyword", ["summer", "winter", "demi-season", "all-season"])
    },
    "Спорттовары": {
        "sport_type": ("keyword",["Футбол", "Баскетбол", "Фитнес", "Йога", "Плавание"]),
        "weight_kg": ("number",[0.5, 1, 2, 5, 10, 20]),
        "material": ("keyword", ["rubber", "plastic", "metal", "fabric"]),
        "level": ("keyword",["beginner", "amateur", "professional"]),
        "waterproof": ("keyword", ["yes", "no"])
    }
}

BRANDS =["Apple", "Samsung", "Xiaomi", "Bosch", "LG", "Nike", "Adidas", "Puma", "Asus", "Lenovo"]
units = {
        "memory": "GB", "ram": "GB", "storage_capacity": "GB",
        "screen_size": '"', "power_w": "W", "weight_kg": "kg", "camera_mp": "MP"
    }

def generate_random_attributes(category_name):
    """Выбирает случайные атрибуты из пула категории и форматирует под nested"""
    nested_attributes =[]
    pool = ATTRIBUTES_POOL.get(category_name, {})

    # Берем от 3 до всех возможных характеристик для товара, чтобы они были разными
    num_attributes_to_pick = random.randint(3, len(pool))
    chosen_keys = random.sample(list(pool.keys()), num_attributes_to_pick)

    for key in chosen_keys:
        attr_type, values = pool[key]
        chosen_value = random.choice(values)

        attr_doc = {"key": key}
        if attr_type == "keyword":
            attr_doc["value_keyword"] = chosen_value
        elif attr_type == "number":
            attr_doc["value_number"] = chosen_value
            unit = units.get(key,"")
            attr_doc["value_keyword"] = f"{chosen_value}{unit}".strip()

        nested_attributes.append(attr_doc)

    return nested_attributes

def generate_documents(num_docs=500):
    """Генератор документов для загрузки через bulk API"""
    for _ in range(num_docs):
        category = random.choice(CATEGORIES)
        brand = random.choice(BRANDS)

        # Генерируем название в зависимости от категории
        item_type = ""
        if category["name"] == "Одежда" or category["name"] == "Бытовая техника":
            # Вытаскиваем тип из пула атрибутов, если есть
            item_type = random.choice(ATTRIBUTES_POOL[category["name"]].get("type", ("keyword", ["Товар"]))[1])
        else:
            item_type = category["name"][:-1] if category["name"].endswith('ы') else category["name"] # простой фикс окончания

        product_name = f"{item_type} {brand} {random.randint(100, 9999)}"
        attr = generate_random_attributes(category["name"])
        attr_values = [a["value_keyword"] for a in attr]
        catch_all = f"{category['name']} {brand} {product_name} {' '.join(attr_values)}"
        doc = {
            "_index": INDEX_NAME,
            "_id": str(uuid.uuid4()),
            "_source": {
                "id": str(uuid.uuid4()),
                "category_id": category["id"],
                "category_name": category["name"],
                "brand":brand,
                "name": product_name,
                "description": f"О{product_name} от бренда {brand}",
                "price_cents": random.randint(100000, 20000000),
                "catch_all": " ".join(catch_all.split()),
                "created_at": datetime.now(timezone.utc).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat(),
                "attributes": attr
            }
        }

        yield doc

if __name__ == "__main__":
    print(f"Генерация и загрузка 500 товаров в Elastic (Index: {INDEX_NAME})...")
    try:
        # helpers.bulk сам бьет данные на пачки (по 500 по умолчанию) и шлет в Elastic
        success, _ = helpers.bulk(es, generate_documents(500))
        print(f"Успешно загружено {success} документов!")
    except Exception as e:
        print(f"Ошибка при загрузке: {e}")