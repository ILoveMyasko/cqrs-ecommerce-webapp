from fastapi import FastAPI

from contextlib import asynccontextmanager

from src.api.routes.users_controller import router as users_router
from src.core.db import sessionmanager
from src.models.user import User
from src.api.dependecies.db_dep import DBSessionDep

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.tiangolo.com/advanced/events/
    """
    yield
    if sessionmanager._engine is not None:
        # Close the DB connection
        await sessionmanager.close()
app = FastAPI(lifespan=lifespan)

app.include_router(users_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
