import re
from typing import Any, Dict, List
from uuid import UUID
from faststream.kafka import KafkaRouter
from src.categories.service import CategoryService
from src.globals.elastic import es_manager
from src.products.schemas import ProductRead, ProductElasticDocument, AttributeNested
from src.projector.config import projector_settings
from src.projector.dependencies import CategoryServiceProjectorDep
from src.projector.schemas import DebeziumPayload
from src.projector.startup import resolve_category_name

product_router = KafkaRouter()

@product_router.subscriber(
    projector_settings.PRODUCT_TOPIC
    , group_id=projector_settings.GROUP_ID
    , auto_offset_reset="earliest")
async def process_product_cdc(
        message: Any,
        category_service: CategoryServiceProjectorDep
):
    if message is None or message == b"":
        print("Tombstone product")
        return

    try:
        payload = DebeziumPayload[ProductRead].model_validate(message)
    except Exception as e:
        print(f"Failed to validate Debezium message: {e}")
        return

    if payload.op == "d" and payload.before:
        await _delete_product_from_elastic(payload.before.id)

    elif payload.after:
        await _upsert_product_in_elastic(payload.after, category_service)


async def _delete_product_from_elastic(product_id: UUID):
    await (es_manager.client
    .options(ignore_status=[404])
    .delete(
        index="products",
        id=str(product_id)
    ))

async def _upsert_product_in_elastic(
    product: ProductRead,
    category_service: CategoryService
):
    category_name = await resolve_category_name(product.category_id, category_service)
    nested_attributes = transform_attributes(product.attributes or {})
    catch_all_string = create_catch_all(product, category_name, nested_attributes)
    doc_data = product.model_dump(exclude={"attributes"})
    doc = ProductElasticDocument(
        **doc_data,
        attributes=nested_attributes,
        catch_all=catch_all_string,
        category_name=category_name
    )
    print(doc)
    await es_manager.client.index(
        index="products",
        id=str(product.id),
        document=doc.model_dump(mode="json")
    )

def transform_attributes(raw_attributes: Dict[str, Any]) -> List[AttributeNested]:
    """
    Превращает {"color": "black", "weight": "1.5 kg"}
    в список объектов для Nested field.
    """
    nested_attrs = []
    for key, value in raw_attributes.items():
        val_str = str(value)
        val_num = None

        match = re.search(r"[-+]?\d*\.\d+|\d+", val_str)
        if match:
            try:
                val_num = float(match.group())
            except ValueError:
                val_num = None

        nested_attrs.append(AttributeNested(
            key=key,
            value_keyword=val_str,
            value_number=val_num
        ))
    return nested_attrs

def create_catch_all(product: Any, category_name: str, attrs: List[AttributeNested]) -> str:

    parts = [
        str(product.name),
        str(product.brand or ""),
        str(category_name)
    ]

    parts.extend([a.value_keyword for a in attrs])

    return " ".join(filter(None, parts))