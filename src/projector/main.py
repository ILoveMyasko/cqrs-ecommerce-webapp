from contextlib import asynccontextmanager
from faststream import FastStream
from faststream.kafka import KafkaBroker

from src.projector.categories_listener import category_router
from src.globals.database import sessionmanager
from src.globals.elastic import es_manager
from src.globals.config import settings
from src.projector.products_listener import product_router
from src.projector.startup import setup_debezium_connector

@asynccontextmanager
async def lifespan():
    await setup_debezium_connector()
    es_manager.connect()
    yield
    await es_manager.close()
    await sessionmanager.close()


broker = KafkaBroker(settings.KAFKA_URL)

broker.include_router(category_router)
broker.include_router(product_router)


app = FastStream(broker, lifespan=lifespan)
