from fastapi import HTTPException
from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import paginate

from app.models.users import User as UserModel
from app.repositories.products_repo import ProductRepository
from app.core.exceptions import (ProductOwnershipError,
                                 ProductNotFound,
                                 CategoryNotFound,
                                 AccessDenied)
from app.repositories.review_repo import ReviewRepository
from app.repositories.category_repo import CategoryRepository
from app.schemas import Product as ProductModel, ProductFilter, ProductCreate as ProductCreateSchema


class ProductService:
    def __init__(self, product_repository: ProductRepository,
                 review_repository: ReviewRepository,
                 category_repository: CategoryRepository):
        self._product_repository = product_repository
        self._review_repository = review_repository
        self._category_repository = category_repository
        
    async def get_product_by_owner(self, product_id: int,
                                         current_user: UserModel):
        """ Returns the owners product """
        product = await self._product_repository.get_product_by_seller(product_id, current_user.id)
        if not product:
            raise ProductOwnershipError()
        return product

    async def get_filtered_products(self,
                                    filter_: ProductFilter,
                                    params: Params
                                    ):
        """ Returns filtered and paginated products """
        query = await self._product_repository.get_query_for_pagination()
        query = filter_.filter(query)
        return await paginate(conn=self._product_repository.db, query=query, params=params)

    async def create_product(self, product_data: ProductCreateSchema, user: UserModel):
        if user.role != 'seller' and user.role != 'admin':
            raise AccessDenied()
        category = self._product_repository.get(product_data.category_id)
        if not category:
            raise CategoryNotFound()
        data = product_data.model_dump()
        data.update({'seller_id': user.id})
        new_product = await self._product_repository.create(data)
        return new_product

    async def find_products_by_category(self, category_id: int):
        """ Find and returns all products by category ID"""
        category = await self._category_repository.get(category_id)
        if not category:
            raise CategoryNotFound()
        products = await self._product_repository.get_all_by_category(category_id)
        if not products:
            raise ProductNotFound()
        return products


    async def find_all_active_products(self):
        """ Finds all active products """
        all_products = await self._product_repository.get_all()
        if not all_products:
            raise ProductNotFound()
        return all_products

    async def get_product_by_search(self, search_name: str | None,
                                    search_price: int | float | None):
        #--- поиск по имени ---
        search_name = search_name.strip()
        if not search_name:
            raise ProductNotFound()
        products_name = await self._product_repository.get_searched_products_by_name(search_name)
        if not products_name:
            raise ProductNotFound()
        # --- поиск по цене
        products_price = await self._product_repository.get_searched_products_by_price(search_price)
        if not products_price:
            raise ProductNotFound()
        products_name = [ProductModel.model_validate(p) for p in products_name]
        products_price = [ProductModel.model_validate(p) for p in products_price]
        total_prods = products_name + products_price
        return total_prods


    async def find_active_product(self, product_id: int, search: str | None):
        """ Finds active product by ID """
        product = await self._product_repository.get(product_id)
        if not product:
            raise ProductNotFound()
        return product

    async def calculate_avg_rating(self, product_id: int):
        """ Method for calculating the average rating of a product"""
        product = await self._product_repository.get(product_id)
        if not product:
            raise ProductNotFound()
        reviews = await self._review_repository.get_reviews_by_product_id(product_id)
        if not reviews:
            return 0.0
        total = sum(rev.grade for rev in reviews)
        avg = total / len(reviews)
        return avg

    async def push_product_rating(self, product_id: int):
        """ Method is pushing product rating """
        new_rating = await self.calculate_avg_rating(product_id)
        await self._product_repository.update_product_rating(product_id, new_rating)
        await self._product_repository.db.commit()

    async def update_product(self, product_id: int,
                             product_data: ProductCreateSchema,
                             user: UserModel):
        """ Method is updating product data """
        product = await self._product_repository.get(product_id)
        if not product:
            raise ProductNotFound()
        owner_product = await self._product_repository.get_product_by_seller(product_id, user.id)
        if not owner_product:
            raise ProductOwnershipError()
        category = await self._category_repository.get(product_data.category_id)
        if not category:
            raise CategoryNotFound()

        updated_product = await self._product_repository.update(product_id, product_data.model_dump())
        await self._product_repository.db.commit()  # Обратить внимание! Нужно переделать, чтобы транзакциями управлял не сервис!
        await self._product_repository.db.refresh(updated_product)
        return updated_product

    async def delete_product(self, product_id, user):
        """ Method is deleting product """
        product = await self._product_repository.get(product_id)
        if not product:
            raise ProductNotFound()
        owner_product = self._product_repository.get_product_by_seller(product_id, user.id)
        if not owner_product:
            raise ProductOwnershipError()
        await self._product_repository.delete(product_id)
        await self._product_repository.db.commit()  # Обратить внимание! Нужно переделать, чтобы транзакциями управлял не сервис!











