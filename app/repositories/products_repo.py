from app.repositories.base_repo import BaseSQLRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update as sql_update
from app.database import Base
from app.models.products import Product as ProductModel


class ProductRepository(BaseSQLRepository):
    def __init__(self, db: AsyncSession, model: Base):
        super().__init__(db, model)

    async def create(self, product_data: dict):
        product = ProductModel(**product_data)
        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)
        return product

    async def get(self, id_: int):
        stmt = select(ProductModel).where(ProductModel.id == id_,
                                          ProductModel.is_active == True)
        result = await self.db.scalars(stmt)
        return result.first()

    async def get_query_for_pagination(self):
        stmt = select(ProductModel).where(ProductModel.is_active == True)
        return stmt

    async def get_all(self):
        stmt = select(ProductModel).where(ProductModel.is_active == True)
        result = await self.db.scalars(stmt)
        return result.all()

    async def get_all_by_category(self, id_: int):
        stmt = select(ProductModel).where(ProductModel.category_id == id_,
                                          ProductModel.is_active == True)
        result = await self.db.scalars(stmt)
        return result.all()

    async def get_product_by_seller(self, product_id, user_id):
        stmt = select(ProductModel).where(ProductModel.id == product_id,
                                          ProductModel.seller_id == user_id,
                                          ProductModel.is_active == True)
        result = await self.db.scalars(stmt)
        result = result.first()
        if not result:
            return None
        return result


    async def update(self, id_: int, updated_data: dict):
        stmt = (
            sql_update(ProductModel)
            .where(ProductModel.id == id_,
                   ProductModel.is_active == True)
            .values(**updated_data)
        )
        await self.db.execute(stmt)
        return await self.get(id_)

    async def update_product_rating(self, id_, rating):
        stmt = (
            sql_update(ProductModel)
            .where(ProductModel.id == id_,
                   ProductModel.is_active == True
                   )
            .values(rating=rating)
        )
        await self.db.execute(stmt)


    async def delete(self, id_: int):
        product = await self.get(id_)
        if not product:
            return None
        product.is_active = False
        self.db.add(product)
        return product