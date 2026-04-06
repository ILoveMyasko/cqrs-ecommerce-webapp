from src.categories.repository import CategoryRepository


class CategoryService:
    def __init__(self, repository: CategoryRepository):
        self.repository= repository

    async def get_category_by_id(self, id:int):
        return ...

    async def create_category(self, ):
        return ...