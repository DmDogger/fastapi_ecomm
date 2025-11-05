from unittest.mock import AsyncMock
import pytest
from faker import Faker
from fastapi.testclient import TestClient
from app.main import app
from app.core.dependecies.services.product_service import get_product_service


Faker.seed(100)


@pytest.fixture(scope='session')
def fake() -> Faker:
    return Faker()

@pytest.fixture(scope='session')
def expected_product_data(fake: Faker) -> dict:
    return {
        'name': fake.sentence(nb_words=5),
        'description': fake.text(max_nb_chars=150),
        'price': str(fake.pyfloat(left_digits=3, right_digits=2, positive=True)),
        'image_url': fake.image_url(),
        'stock': fake.pyint(min_value=1, max_value=500),
        'is_active': True,
        'category_id': fake.pyint(min_value=1, max_value=10),
        'rating': float(fake.pyfloat(min_value=1.0, max_value=5.0, positive=True))
    }


@pytest.fixture(scope='session')
def mock_product_service(expected_product_data) -> AsyncMock:
    mock_service = AsyncMock()

    mock_service.find_active_product.return_value = expected_product_data
    return mock_service


@pytest.fixture(scope='module')
def client(mock_product_service: AsyncMock) -> TestClient:
    def override_get_product_service():
        return mock_product_service

    app.dependency_overrides[get_product_service] = override_get_product_service

    with TestClient(app) as client_instance:
        yield client_instance

    app.dependency_overrides.clear()