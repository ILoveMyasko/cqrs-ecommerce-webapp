from uuid import UUID
from typing import Any
from faststream.kafka import KafkaRouter
from src.categories.schemas import CategoryElasticDocument, CategoryRead
from src.categories.service import CategoryService
from src.globals.elastic import es_manager
from src.projector.dependencies import CategoryServiceProjectorDep
from src.projector.schemas import DebeziumPayload
from src.projector.config import projector_settings
from src.projector.startup import category_name_cache, resolve_category_name

category_router = KafkaRouter()

@category_router.subscriber(
    projector_settings.CATEGORY_TOPIC
    , group_id=projector_settings.GROUP_ID
    , auto_offset_reset="earliest")
async def process_category_cdc(
    message: Any,
    category_service: CategoryServiceProjectorDep
):
    if message is None or message == b"":
        print("Tombstone category")
        return
    try:
        payload = DebeziumPayload[CategoryRead].model_validate(message)
    except Exception as e:
        print(f"Failed to validate Debezium message: {e}")
        return


    if payload.op == "d" and payload.before:
        await _delete_category_from_elastic(payload.before.id)
        category_name_cache.pop(payload.before.id, None)
        return

    # operation = update/create/read
    elif payload.after:
        category_data = payload.after
        await _upsert_category_in_elastic(category_data, category_service)

        if (
            payload.op == "u"
            and payload.before
            and payload.before.name != category_data.name
        ):
            await _update_products_category_name_update(category_data)


async def _delete_category_from_elastic(category_id : UUID):
    await (es_manager.client
    .options(ignore_status=[404])
    .delete(
        index="categories",
        id=str(category_id)
    ))

async def _upsert_category_in_elastic(category: CategoryRead, category_service: CategoryService):
    parent_name = await resolve_category_name(category.id, category_service)

    doc = CategoryElasticDocument(
        **category.model_dump(),
        parent_name=parent_name
    )

    await es_manager.client.index(
        index="categories",
        id=str(category.id),
        document=doc.model_dump(mode="json")
    )

async def _update_products_category_name_update(category_data: CategoryRead):
    category_name_cache[category_data.id]=category_data.name
    await es_manager.client.update_by_query(
                index="categories",
                query={"term": {"parent_id": str(category_data.id)}},
                script={
                    "source": "ctx._source.parent_name = params.new_name",
                    "params": {"new_name": category_data.name}
                },
                wait_for_completion=False,
                conflicts="proceed"
            )