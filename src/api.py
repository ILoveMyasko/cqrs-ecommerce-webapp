import asyncio

from fastapi import FastAPI

from contextlib import asynccontextmanager

from src.users.router import router as users_router
from src.categories.router import router as categories_router
from src.globals.database import sessionmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    #consumer_task = asyncio.create_task()
    yield
    if sessionmanager._engine is not None:
        await sessionmanager.close()
        #TODO: elastic handle

app = FastAPI(lifespan=lifespan)

app.include_router(users_router)
app.include_router(categories_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
