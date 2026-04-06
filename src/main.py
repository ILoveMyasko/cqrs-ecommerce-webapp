from fastapi import FastAPI

from contextlib import asynccontextmanager

from src.users.router import router as users_router
from src.database import sessionmanager
from src.api.dependecies.db_dep import DBSessionDep

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if sessionmanager._engine is not None:
        await sessionmanager.close()
app = FastAPI(lifespan=lifespan)

app.include_router(users_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
