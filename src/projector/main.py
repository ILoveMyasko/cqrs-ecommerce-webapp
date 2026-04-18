from contextlib import asynccontextmanager
from faststream import FastStream
from faststream.kafka import KafkaBroker

from src.projector.handlers import category_router
from src.globals.database import sessionmanager
from src.globals.elastic import es_manager
from src.globals.config import settings
from src.projector.setup import setup_debezium

broker = KafkaBroker(settings.KAFKA_URL)
broker.include_router(category_router)


@asynccontextmanager
async def lifespan():
    await setup_debezium()
    es_manager.connect()
    yield
    await es_manager.close()
    await sessionmanager.close()

app = FastStream(broker, lifespan=lifespan)
