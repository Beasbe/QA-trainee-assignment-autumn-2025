import pytest
from api_client import ApiClient

@pytest.mark.positive
class TestApiV2Positive:
    """Позитивные тесты для API v2"""

    def test_delete_ad_success(self, api_client, sample_ad_data):
        """Тест успешного удаления объявления (v2)"""
        # Создаем объявление для удаления
        create_response = api_client.create_ad(sample_ad_data)
        assert create_response.status_code == 200
        create_data = create_response.json()
        ad_id = api_client.extract_ad_id(create_data)
        assert ad_id is not None

        # Удаляем объявление
        delete_response = api_client.delete_ad(ad_id)

        # Assert
        assert delete_response.status_code == 200

        # Проверяем, что объявление действительно удалено
        get_response = api_client.get_ad_by_id(ad_id)
        assert get_response.status_code in [404, 400]

    def test_get_statistics_v2_success(self, api_client, sample_ad_data):
        """Тест получения статистики по объявлению (v2)"""
        # Создаем объявление
        create_response = api_client.create_ad(sample_ad_data)
        assert create_response.status_code == 200
        create_data = create_response.json()
        ad_id = api_client.extract_ad_id(create_data)

        # Получаем статистику через v2
        response = api_client.get_statistics_v2(ad_id)

        # Assert
        # Статус может быть 200 или 404 если статистики нет
        assert response.status_code in [200, 404]

        if response.status_code == 200:
            data = response.json()
            assert isinstance(data, list)
            # Проверяем структуру статистики если она есть
            for stat in data:
                assert "likes" in stat
                assert "viewCount" in stat
                assert "contacts" in stat

        # Cleanup
        api_client.delete_ad(ad_id)

@pytest.mark.negative
class TestApiV2Negative:
    """Негативные тесты для API v2"""

    def test_delete_nonexistent_ad(self, api_client):
        """Тест удаления несуществующего объявления"""
        response = api_client.delete_ad("nonexistent_id_12345")
        # Может быть 404 или 400
        assert response.status_code in [400, 404]

    def test_get_statistics_v2_nonexistent_ad(self, api_client):
        """Тест получения статистики несуществующего объявления (v2)"""
        response = api_client.get_statistics_v2("nonexistent_id_12345")
        assert response.status_code in [400, 404]

@pytest.mark.integration
class TestApiV2Integration:
    """Интеграционные тесты для API v2"""

    def test_statistics_v1_v2_consistency(self, api_client, sample_ad_data):
        """Тест согласованности статистики между v1 и v2"""
        # Создаем объявление
        create_response = api_client.create_ad(sample_ad_data)
        assert create_response.status_code == 200
        create_data = create_response.json()
        ad_id = api_client.extract_ad_id(create_data)

        try:
            # Получаем статистику через v1
            stats_v1_response = api_client.get_statistics_v1(ad_id)
            stats_v1 = stats_v1_response.json() if stats_v1_response.status_code == 200 else None

            # Получаем статистику через v2
            stats_v2_response = api_client.get_statistics_v2(ad_id)
            stats_v2 = stats_v2_response.json() if stats_v2_response.status_code == 200 else None

            # Оба эндпоинта должны возвращать одинаковые статусы
            # (либо оба 200, либо оба 404 и т.д.)
            assert stats_v1_response.status_code == stats_v2_response.status_code

            # Если оба вернули данные, они должны быть согласованы
            if stats_v1_response.status_code == 200 and stats_v2_response.status_code == 200:
                assert isinstance(stats_v1, list)
                assert isinstance(stats_v2, list)
                # Можно добавить более детальную проверку структуры данных

        finally:
            # Cleanup
            api_client.delete_ad(ad_id)

    def test_complete_ad_lifecycle_v2(self, api_client, sample_ad_data):
        """Полный цикл жизни объявления с использованием v2 для удаления"""
        # 1. Создаем объявление (v1)
        create_response = api_client.create_ad(sample_ad_data)
        assert create_response.status_code == 200
        create_data = create_response.json()
        ad_id = api_client.extract_ad_id(create_data)

        # 2. Получаем объявление (v1)
        get_response = api_client.get_ad_by_id(ad_id)
        assert get_response.status_code == 200

        # 3. Получаем статистику (v2)
        stats_response = api_client.get_statistics_v2(ad_id)
        assert stats_response.status_code in [200, 404]

        # 4. Удаляем объявление (v2)
        delete_response = api_client.delete_ad(ad_id)
        assert delete_response.status_code == 200

        # 5. Проверяем, что объявление удалено
        get_after_delete = api_client.get_ad_by_id(ad_id)
        assert get_after_delete.status_code in [404, 400]


@pytest.mark.smoke
class TestApiV2Smoke:
    """Smoke-тесты для API v2"""

    def test_smoke_delete_functionality(self, api_client, sample_ad_data):
        """Smoke-тест: проверка функциональности удаления"""
        # Создаем и сразу удаляем объявление
        create_response = api_client.create_ad(sample_ad_data)
        assert create_response.status_code == 200
        create_data = create_response.json()
        ad_id = api_client.extract_ad_id(create_data)

        delete_response = api_client.delete_ad(ad_id)
        assert delete_response.status_code == 200

    def test_smoke_statistics_v2(self, api_client):
        """Smoke-тест: проверка доступности statistics v2"""
        # Простой запрос для проверки подключения
        response = api_client.get_statistics_v2("test_id")
        assert response.status_code in [200, 400, 404]  # Любой ответ кроме 5xx