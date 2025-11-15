import pytest
import random
from api_client import ApiClient

@pytest.fixture
def api_client():
    """Фикстура для API клиента"""
    return ApiClient()

@pytest.fixture
def unique_seller_id():
    """Генерирует уникальный sellerID в диапазоне 111111-999999"""
    return random.randint(111111, 999999)

@pytest.fixture
def sample_ad_data(unique_seller_id):
    """Фикстура с тестовыми данными для объявления"""
    return {
        "sellerID": unique_seller_id,
        "name": "Test Product",
        "price": 1000,
        "statistics": {
            "likes": 10,
            "viewCount": 100,
            "contacts": 5
        }
    }

def pytest_configure(config):
    """Конфигурация pytest"""
    config.addinivalue_line("markers", "smoke: маркер для smoke-тестов")
    config.addinivalue_line("markers", "negative: маркер для негативных тестов")