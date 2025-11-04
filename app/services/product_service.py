from app.models.users import User as UserModel
from app.repositories.products_repo import ProductRepository
from app.core.exceptions import (ProductOwnershipError,
                                 ProductNotFound)
from app.repositories.review_repo import ReviewRepository


class ProductService:
    def __init__(self, product_repository: ProductRepository, review_repository: ReviewRepository):
        self._product_repository = product_repository
        self._review_repository = review_repository

    async def get_product_by_owner(self, product_id: int,
                                         current_user: UserModel):
        """ Возвращает продукт владельца """
        product = await self._product_repository.get_product_by_seller(product_id, current_user.id)
        if not product:
            raise ProductOwnershipError()

    async def find_all_active_products(self):
        """ Находит все активные товары """
        all_products = await self._product_repository.get_all()
        if not all_products:
            raise ProductNotFound()
        return all_products


    async def find_active_product(self, product_id: int):
        """ Находит активный товар """
        product = await self._product_repository.get(product_id)
        if not product:
            raise ProductNotFound()
        return product

    async def calculate_avg_rating(self, product_id: int):
        """ Метод для расчета среднего рейтинга продукта"""
        product = await self._product_repository.get(product_id)
        if not product:
            raise ProductNotFound()
        reviews = await self._review_repository.get_reviews_by_product_id(product_id)
        if not reviews:
            return 0.0
        total = sum(rev.grade for rev in reviews)
        avg = total / len(reviews)
        return avg

    async def push_product_rating(self, product_id):
        new_rating = await self.calculate_avg_rating(product_id)
        await self._product_repository.update_product_rating(product_id, new_rating)
        await self._product_repository.db.commit()








