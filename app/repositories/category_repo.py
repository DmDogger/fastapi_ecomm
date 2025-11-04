from app.repositories.base_repo import BaseSQLRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update as sql_update
from app.models.categories import Category as CategoryModel


class CategoryRepository(BaseSQLRepository):
    def __init__(self, db: AsyncSession, model: CategoryModel):
        super().__init__(db, model)

    async def get(self, id_):
        stmt = select(CategoryModel).where(CategoryModel.id == id_,
                                           CategoryModel.is_active == True)
        return await self.db.scalar(stmt)

    async def get_category_by_parent(self, id_: int):
        stmt = select(CategoryModel).where(CategoryModel.id == id_,
                                           CategoryModel.is_active == True)
        result = await self.db.scalars(stmt)
        return result.first()

    async def create(self, category):
        category_orm = CategoryModel(**category.model_dump())
        self.db.add(category_orm)
        await self.db.commit()
        return category_orm

    async def update(self, id_: int, updated_data: dict):
        stmt = (
            sql_update(CategoryModel).
            where(CategoryModel.id == id_,
                  CategoryModel.is_active == True)
            .values(**updated_data)
        )
        await self.db.execute(stmt)
        return await self.get(id_)

    async def get_all(self):
        stmt = select(CategoryModel).where(CategoryModel.is_active == True)
        result = await self.db.scalars(stmt)
        result = result.all()
        return result

    async def delete(self, id_: int):
        category = await self.get(id_)
        if not category:
            return None
        category.is_active = False
        self.db.add(category)
        return category

    def get_query_for_pagination(self):
        query = select(CategoryModel).where(CategoryModel.is_active == True)
        return query
