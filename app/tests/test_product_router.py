from fastapi.testclient import TestClient
from unittest.mock import AsyncMock


def test_get_product_success(
        client: TestClient,
        expected_product_data: dict,
        mock_product_service: AsyncMock
):
    response = client.get('/products/search/5')


    assert response.status_code == 200
    assert response.json() == expected_product_data
    assert response.headers['content-type'] == 'application/json'


