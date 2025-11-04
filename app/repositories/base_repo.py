from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import Base

class BaseSQLRepository(ABC):
    def __init__(self, db: AsyncSession, model: Base):
        self.db = db
        self.model = model

    @abstractmethod
    async def create(self, **kwargs):
        """
        Абстрактный метод для работы с ORM.
        Позволяет создавать объекты
        """
        raise NotImplemented

    @abstractmethod
    async def get(self, id_: int):
        """
        Абстрактный метод для работы с ORM.
        Позволяет получать объект
        """
        raise NotImplemented

    @abstractmethod
    async def get_all(self):
        """
        Абстрактный метод для работы с ORM.
        Позволяет получить все объекты
        """

        raise NotImplemented

    @abstractmethod
    async def update(self, id_: int, updated_data: dict):
        """
        Абстрактный метод для работы с ORM.
        Позволяет обновлять объекты
        """
        raise NotImplemented

    @abstractmethod
    async def delete(self, id_: int):
        """
        Абстрактный метод для работы с ORM.
        Позволяет обновлять объекты
        """
        raise NotImplemented
