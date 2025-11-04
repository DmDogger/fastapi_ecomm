from fastapi import Depends
from app.database import AsyncSession
from app.db_depends import get_async_db
from app.repositories.products_repo import ProductRepository
from app.models.products import Product as ProductModel

def get_product_repository(
        session: AsyncSession = Depends(get_async_db)
) -> ProductRepository:
    """ Конструкция ProductRepository с внедренной AsyncSession """
    return ProductRepository(db=session, model=ProductModel)



