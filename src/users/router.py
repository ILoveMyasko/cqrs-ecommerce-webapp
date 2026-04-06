from fastapi import APIRouter
from pydantic import EmailStr

from src.users.dependencies import UserServiceDep
from src.users.schemas import UserRead, UserCreate
router = APIRouter(
    prefix="/users",
)


@router.get("/{user_id}", response_model=UserRead)
async def get_user_by_id(
        user_service: UserServiceDep,
        user_id: int
):
    return await user_service.get_user_by_id(user_id)  # auto transform??


@router.get("/", response_model=UserRead)
async def get_user_by_email(
        user_service: UserServiceDep,
        email: EmailStr,
):
    return await user_service.get_user_by_email(email)


@router.post("/", response_model=UserRead, status_code=201)
async def add_user(
        user_service: UserServiceDep,
        create_user_dto: UserCreate
):
    created_user = await user_service.create_user(create_user_dto)
    print(f"DEBUG: result is {created_user}")
    return created_user
