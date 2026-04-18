import uuid
from typing import Any

from cachetools import TTLCache
from faststream.kafka import KafkaRouter

from src.categories.schemas import CategoryElasticDocument, CategoryRead
from src.globals.elastic import es_manager
from src.projector.dependencies import CategoryRepoDep
from src.projector.schemas import DebeziumPayload
from src.projector.config import projector_settings

category_router = KafkaRouter()
category_name_cache = TTLCache(maxsize=5000, ttl=3600)

@category_router.subscriber(
    projector_settings.CATEGORY_TOPIC
    , group_id="v4"
    , auto_offset_reset="earliest")
async def process_category_cdc(
    message: Any,
    repository: CategoryRepoDep
):
    if message is None or message == b"":
        return
    print("not None at least")
    try:
        payload = DebeziumPayload[CategoryRead].model_validate(message)
    except Exception as e:
        print(f"Failed to validate Debezium message: {e}")
        return


    if payload.op == "d":
        if not payload.before:
            return
        category_id = str(payload.before.id)
        await (es_manager.client
               .options(ignore_status=[404])
               .delete(index="categories"
                       , id=category_id
                       ))
        category_name_cache.pop(payload.before.id, None)
        return

    # operation = update/create/read
    if not payload.after:
        return


    category_data = payload.after

    parent_name = None
    if category_data.parent_id:
        parent_name = await get_cached_category_name(category_data.parent_id, repository)

    doc = CategoryElasticDocument(
        **category_data.model_dump(),
        parent_name=parent_name
    )

    await es_manager.client.index(
        index="categories",
        id=str(category_data.id),
        document=doc.model_dump(mode="json")
    )

    if (
        payload.op == "u"
        and payload.before
        and payload.before.name != category_data.name
    ):
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


async def get_cached_category_name(category_id: uuid.UUID, repository: CategoryRepoDep) -> str | None:
    if name := category_name_cache.get(category_id):
        return name

    category = await repository.get_by_uuid(category_id)
    if category:
        category_name_cache[category_id] = category.name
        return category.name
    return None