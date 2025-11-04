from app.repositories.review_repo import ReviewRepository

from app.services.review_service import ReviewService


def get_review_service(
        repository=ReviewRepository
) -> ReviewService:
    """
    Создает экземпляр ReviewService с внедренными репозиториями.
    """
    return ReviewService(repository)