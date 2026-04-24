import asyncio
import uuid

import httpx
from cachetools import TTLCache
from fastapi import HTTPException

from src.categories.service import CategoryService
from src.projector.config import projector_settings
async def setup_debezium_connector():
    status_url = f"{projector_settings.DEBEZIUM_URL}/connectors/{projector_settings.CONNECTOR_NAME}/status"
    config_url = f"{projector_settings.DEBEZIUM_URL}/connectors/{projector_settings.CONNECTOR_NAME}/config"
    async with httpx.AsyncClient() as client:
        for _ in range(10):
            try:
                response = await client.get(status_url)
                await client.put(config_url, json=projector_settings.DEBEZIUM_CONNECTOR_CONFIG)
                print("putted client")
                break
            except httpx.RequestError:
                print("not successful:")
                await asyncio.sleep(5)


category_name_cache = TTLCache(maxsize=5000, ttl=3600)

async def resolve_category_name(
    category_id: uuid.UUID,
    category_service: CategoryService
) -> str | None:
    if name := category_name_cache.get(category_id):
        return name
    try:
        category = await category_service.get_category_by_uuid(category_id)
        category_name_cache[category_id] = category.name
        return category.name
    except HTTPException as e:
        if e.status_code == 404:
            return None
        raise e
