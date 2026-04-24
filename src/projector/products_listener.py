from typing import Any
from uuid import UUID
from faststream.kafka import KafkaRouter
from src.categories.service import CategoryService
from src.globals.elastic import es_manager
from src.products.schemas import ProductRead, ProductElasticDocument
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

    doc = ProductElasticDocument(
        **product.model_dump(),
        category_name=category_name
    )

    await es_manager.client.index(
        index="products",
        id=str(product.id),
        document=doc.model_dump(mode="json")
    )