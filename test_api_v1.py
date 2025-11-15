import pytest
from api_client import ApiClient

@pytest.mark.positive
class TestApiV1Positive:
    """Позитивные тесты для API v1"""

    def test_create_ad_success(self, api_client, sample_ad_data):
        """Тест успешного создания объявления"""
        # Act
        response = api_client.create_ad(sample_ad_data)

        # Assert
        assert response.status_code == 200
        data = response.json()

        # Проверяем новый формат ответа
        assert "status" in data
        assert "Сохранили объявление" in data["status"]

        # Извлекаем ID из статуса
        ad_id = api_client.extract_ad_id(data)
        assert ad_id is not None

        # Cleanup
        api_client.delete_ad(ad_id)

    def test_get_ad_by_id_success(self, api_client, sample_ad_data):
        """Тест получения объявления по ID"""
        # Создаем объявление
        create_response = api_client.create_ad(sample_ad_data)
        assert create_response.status_code == 200
        create_data = create_response.json()
        ad_id = api_client.extract_ad_id(create_data)

        # Получаем объявление по ID
        response = api_client.get_ad_by_id(ad_id)

        # Assert
        assert response.status_code == 200
        data = response.json()

        # Формат ответа может быть массивом или объектом
        if isinstance(data, list):
            assert len(data) > 0
            ad_data = data[0]
        else:
            ad_data = data

        assert "id" in ad_data
        assert ad_data["id"] == ad_id

        # Cleanup
        api_client.delete_ad(ad_id)

    def test_get_ads_by_seller_success(self, api_client, sample_ad_data):
        """Тест получения всех объявлений продавца"""
        # Создаем объявление
        create_response = api_client.create_ad(sample_ad_data)
        assert create_response.status_code == 200
        seller_id = sample_ad_data["sellerID"]

        # Получаем объявления продавца
        response = api_client.get_ads_by_seller(seller_id)

        # Assert
        assert response.status_code == 200
        data = response.json()

        assert isinstance(data, list)
        # Может быть пустым или содержать объявления

        # Cleanup - находим ID созданного объявления для удаления
        create_data = create_response.json()
        ad_id = api_client.extract_ad_id(create_data)
        api_client.delete_ad(ad_id)

    def test_get_statistics_v1_success(self, api_client, sample_ad_data):
        """Тест получения статистики по объявлению (v1)"""
        # Создаем объявление
        create_response = api_client.create_ad(sample_ad_data)
        assert create_response.status_code == 200
        create_data = create_response.json()
        ad_id = api_client.extract_ad_id(create_data)

        # Получаем статистику
        response = api_client.get_statistics_v1(ad_id)

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
class TestApiV1Negative:
    """Негативные тесты для API v1"""

    @pytest.mark.parametrize("negative_price", [-1, -100, -999999])
    def test_create_ad_negative_price(self, api_client, unique_seller_id, negative_price):
        """Тест создания объявления с отрицательной ценой"""
        # Arrange
        invalid_data = {
            "sellerID": unique_seller_id,
            "name": f"Product with negative price {negative_price}",
            "price": negative_price,
            "statistics": {
                "likes": 10,
                "viewCount": 100,
                "contacts": 5
            }
        }

        # Act
        response = api_client.create_ad(invalid_data)

        # Assert
        assert response.status_code == 400, f"BUG: API accepts negative price {negative_price}!"

    @pytest.mark.parametrize("seller_id,expected_status,description", [
        (999999, 404, "Nonexistent seller should return 404"),
        (0, 404, "Zero seller ID should return 404"),
        (-123, 404, "Negative seller ID should return 404"),
    ])
    def test_get_ads_invalid_sellers(self, api_client, seller_id, expected_status, description):
        """Параметризованный тест для различных невалидных seller ID"""
        # Act
        response = api_client.get_ads_by_seller(seller_id)

        # Assert
        assert response.status_code == expected_status, (
            f"{description}. Expected {expected_status}, got {response.status_code}"
        )

    @pytest.mark.parametrize("negative_likes", [-1, -10, -100])
    def test_create_ad_negative_likes(self, api_client, unique_seller_id, negative_likes):
        """Тест создания объявления с отрицательным количеством лайков"""
        # Arrange
        invalid_data = {
            "sellerID": unique_seller_id,
            "name": f"Product with negative likes {negative_likes}",
            "price": 100,
            "statistics": {
                "likes": negative_likes,
                "viewCount": 100,
                "contacts": 5
            }
        }

        # Act
        response = api_client.create_ad(invalid_data)

        # Assert
        assert response.status_code == 400, f"BUG: API accepts negative likes {negative_likes}!"

    @pytest.mark.parametrize("negative_view_count", [-1, -50, -1000])
    def test_create_ad_negative_viewCount(self, api_client, unique_seller_id, negative_view_count):
        """Тест создания объявления с отрицательным количеством просмотров"""
        # Arrange
        invalid_data = {
            "sellerID": unique_seller_id,
            "name": f"Product with negative views {negative_view_count}",
            "price": 100,
            "statistics": {
                "likes": 10,
                "viewCount": negative_view_count,
                "contacts": 5
            }
        }

        # Act
        response = api_client.create_ad(invalid_data)

        # Assert
        assert response.status_code == 400, f"BUG: API accepts negative viewCount {negative_view_count}!"

    @pytest.mark.parametrize("negative_contacts", [-1, -5, -100])
    def test_create_ad_negative_contacts(self, api_client, unique_seller_id, negative_contacts):
        """Тест создания объявления с отрицательным количеством контактов"""
        # Arrange
        invalid_data = {
            "sellerID": unique_seller_id,
            "name": f"Product with negative contacts {negative_contacts}",
            "price": 100,
            "statistics": {
                "likes": 10,
                "viewCount": 100,
                "contacts": negative_contacts
            }
        }

        # Act
        response = api_client.create_ad(invalid_data)

        # Assert
        assert response.status_code == 400, f"BUG: API accepts negative contacts {negative_contacts}!"

    @pytest.mark.parametrize("negative_seller_id", [-1, -123456, -999999])
    def test_create_ad_negative_sellerid(self, api_client, negative_seller_id):
        """Тест создания объявления с отрицательным sellerID"""
        # Arrange
        invalid_data = {
            "sellerID": negative_seller_id,
            "name": f"Product with negative sellerID {negative_seller_id}",
            "price": 100,
            "statistics": {
                "likes": 10,
                "viewCount": 100,
                "contacts": 5
            }
        }

        # Act
        response = api_client.create_ad(invalid_data)

        # Assert
        assert response.status_code == 400, f"BUG: API accepts negative sellerID {negative_seller_id}!"

    @pytest.mark.parametrize("zero_value_field,zero_value", [
        ("sellerID", 0),
        ("price", 0),
        ("likes", 0),
        ("viewCount", 0),
        ("contacts", 0)
    ])
    def test_create_ad_zero_values(self, api_client, unique_seller_id, zero_value_field, zero_value):
        """Тест создания объявления с нулевыми значениями для разных полей"""
        # Arrange
        base_data = {
            "sellerID": unique_seller_id,
            "name": f"Product with zero {zero_value_field}",
            "price": 100,
            "statistics": {
                "likes": 10,
                "viewCount": 100,
                "contacts": 5
            }
        }

        # Устанавливаем нулевое значение для целевого поля
        if zero_value_field == "sellerID":
            base_data["sellerID"] = zero_value
        elif zero_value_field == "price":
            base_data["price"] = zero_value
        else:
            base_data["statistics"][zero_value_field] = zero_value

        # Act
        response = api_client.create_ad(base_data)

        # Assert - определяем ожидаемый результат для каждого поля
        expected_status = 400 if zero_value_field in ["sellerID"] else 200
        assert response.status_code == expected_status, \
            f"Unexpected behavior for zero {zero_value_field}: expected {expected_status}, got {response.status_code}"

        # Cleanup если создание прошло успешно
        if response.status_code == 200:
            ad_id = api_client.extract_ad_id(response.json())
            api_client.delete_ad(ad_id)

    def test_create_ad_multiple_negative_values(self, api_client):
        """Тест нескольких отрицательных значений одновременно"""
        # Arrange
        invalid_data = {
            "sellerID": -999999,
            "name": "Multiple Negative Values Product",
            "price": -1000,
            "statistics": {
                "likes": -999,
                "viewCount": -999,
                "contacts": -999
            }
        }

        # Act
        response = api_client.create_ad(invalid_data)

        # Assert
        assert response.status_code == 400, "CRITICAL BUG: API accepts ALL negative values!"

    @pytest.mark.parametrize("field_combinations", [
        {"sellerID": -123, "price": 100, "likes": 10, "viewCount": 100, "contacts": 5},
        {"sellerID": 123, "price": -100, "likes": 10, "viewCount": 100, "contacts": 5},
        {"sellerID": 123, "price": 100, "likes": -10, "viewCount": 100, "contacts": 5},
        {"sellerID": 123, "price": 100, "likes": 10, "viewCount": -100, "contacts": 5},
        {"sellerID": 123, "price": 100, "likes": 10, "viewCount": 100, "contacts": -5},
        {"sellerID": -123, "price": -100, "likes": 10, "viewCount": 100, "contacts": 5},
    ])
    def test_create_ad_negative_combinations(self, api_client, field_combinations):
        """Тест комбинаций отрицательных значений"""
        # Arrange
        invalid_data = {
            "sellerID": field_combinations["sellerID"],
            "name": f"Combination test product",
            "price": field_combinations["price"],
            "statistics": {
                "likes": field_combinations["likes"],
                "viewCount": field_combinations["viewCount"],
                "contacts": field_combinations["contacts"]
            }
        }

        # Act
        response = api_client.create_ad(invalid_data)

        # Assert
        assert response.status_code == 400, f"BUG: API accepts negative combination: {field_combinations}"
@pytest.mark.integration
class TestApiV1Integration:
    """Интеграционные тесты полного цикла"""

    def test_full_ad_lifecycle(self, api_client, sample_ad_data):
        """Полный цикл: создание -> получение -> удаление"""
        # 1. Создаем объявление
        create_response = api_client.create_ad(sample_ad_data)
        assert create_response.status_code == 200
        create_data = create_response.json()
        ad_id = api_client.extract_ad_id(create_data)
        assert ad_id is not None

        # 2. Получаем объявление
        get_response = api_client.get_ad_by_id(ad_id)
        assert get_response.status_code == 200

        # 3. Удаляем объявление
        delete_response = api_client.delete_ad(ad_id)
        assert delete_response.status_code == 200

        # 4. Проверяем, что объявление удалено
        get_after_delete = api_client.get_ad_by_id(ad_id)
        assert get_after_delete.status_code in [404, 400]

@pytest.mark.security
class TestApiV1Security:
    """Тесты безопасности и валидации данных"""

    @pytest.mark.parametrize("invalid_name", [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert(1)>",
        "Avito" * 200,  # Очень длинное имя
        "Avito" * 2000,  # Сверхдлинное имя
        "'; DROP TABLE ads; --",  # SQL injection
        "Test\tName\nWith\tSpecial\tChars",
        "   ",  # Только пробелы
        "",  # Пустая строка
    ])
    def test_create_ad_invalid_name_values(self, api_client, unique_seller_id, invalid_name):
        """Тест валидации поля name на XSS, инъекции и длину"""
        # Arrange
        test_data = {
            "sellerID": unique_seller_id,
            "name": invalid_name,
            "price": 100,
            "statistics": {
                "likes": 10,
                "viewCount": 100,
                "contacts": 5
            }
        }

        # Act
        response = api_client.create_ad(test_data)

        # Assert
        if response.status_code == 200:
            # Если создалось - извлекаем ID и проверяем санитизацию
            ad_id = api_client.extract_ad_id(response.json())

            # Получаем созданное объявление для проверки
            get_response = api_client.get_ad_by_id(ad_id)
            if get_response.status_code == 200:
                ad_data = get_response.json()
                if isinstance(ad_data, list):
                    ad_data = ad_data[0]

                # Проверяем что опасные символы были санитизированы
                created_name = ad_data.get("name", "")
                if "<script>" in invalid_name.lower():
                    assert "<script>" not in created_name, "XSS vulnerability: script tags not sanitized"
                if "onerror" in invalid_name.lower():
                    assert "onerror" not in created_name, "XSS vulnerability: onerror not sanitized"

            # Cleanup
            api_client.delete_ad(ad_id)
            print(f"WARNING: Potential security issue - created ad with name: {invalid_name[:50]}...")
        else:
            # Ожидаем 400 для невалидных значений
            assert response.status_code == 400, f"Should reject invalid name but got {response.status_code}"

    def test_create_ad_name_length_boundaries(self, api_client, unique_seller_id):
        """Тест граничных значений длины поля name"""
        test_cases = [
            {"name": "A", "should_work": True, "description": "Min length (1 char)"},
            {"name": "Avito" * 51, "should_work": True, "description": "Max reasonable length (255 chars)"},
            {"name": "A" * 256, "should_work": False, "description": "Over max length (256 chars)"},
            {"name": "A" * 1000, "should_work": False, "description": "Very long name (1000 chars)"},
            {"name": "", "should_work": False, "description": "Empty name"},
            {"name": "   ", "should_work": False, "description": "Only spaces"},
        ]

        for case in test_cases:
            # Arrange
            test_data = {
                "sellerID": unique_seller_id,
                "name": case["name"],
                "price": 100,
                "statistics": {
                    "likes": 10,
                    "viewCount": 100,
                    "contacts": 5
                }
            }

            # Act
            response = api_client.create_ad(test_data)

            # Assert
            if case["should_work"]:
                assert response.status_code == 200, f"Valid name case failed: {case['description']}"
                # Cleanup
                ad_id = api_client.extract_ad_id(response.json())
                api_client.delete_ad(ad_id)
            else:
                assert response.status_code == 400, f"BUG: Invalid name was accepted: {case['description']}"

    @pytest.mark.parametrize("large_seller_id", [
        999999999999999999,  # Очень большое число
        2 ** 31,  # Превышение INT32
        2 ** 63,  # Превышение INT64
        "999999999999999999",  # Большое число как строка
    ])
    def test_create_ad_very_large_seller_id(self, api_client, large_seller_id):
        """Тест обработки очень больших sellerID"""
        # Arrange
        test_data = {
            "sellerID": large_seller_id,
            "name": "Product with large sellerID",
            "price": 100,
            "statistics": {
                "likes": 10,
                "viewCount": 100,
                "contacts": 5
            }
        }

        # Act
        response = api_client.create_ad(test_data)

        # Assert
        if response.status_code == 400:
            # Проверяем что ошибка понятная, а не "не передано тело объявления"
            response_text = response.text
            assert "не передано тело объявления" not in response_text, (
                f"BUG: Misleading error message for large sellerID {large_seller_id}"
            )
        elif response.status_code == 200:
            # Если создалось - проверяем что sellerID сохранился корректно
            ad_id = api_client.extract_ad_id(response.json())
            get_response = api_client.get_ad_by_id(ad_id)

            if get_response.status_code == 200:
                ad_data = get_response.json()
                if isinstance(ad_data, list):
                    ad_data = ad_data[0]

                # Проверяем что sellerID сохранился как есть
                assert "sellerID" in ad_data
                print(f"INFO: Large sellerID {large_seller_id} was accepted and stored as {ad_data['sellerID']}")

            # Cleanup
            api_client.delete_ad(ad_id)

    def test_create_ad_numeric_boundaries_seller_id(self, api_client):
        """Тест числовых границ для sellerID"""
        test_cases = [
            {"seller_id": 1, "should_work": True, "description": "Min valid ID"},
            {"seller_id": 2147483647, "should_work": True, "description": "MAX INT32"},
            {"seller_id": 2147483648, "should_work": False, "description": "Over MAX INT32"},
            {"seller_id": 999999999, "should_work": True, "description": "Large but reasonable"},
            {"seller_id": 999999999999, "should_work": False, "description": "Very large ID"},
            {"seller_id": 0, "should_work": False, "description": "Zero ID"},
            {"seller_id": -1, "should_work": False, "description": "Negative ID"},
        ]

        for case in test_cases:
            # Arrange
            test_data = {
                "sellerID": case["seller_id"],
                "name": f"Product with sellerID {case['seller_id']}",
                "price": 100,
                "statistics": {
                    "likes": 10,
                    "viewCount": 100,
                    "contacts": 5
                }
            }

            # Act
            response = api_client.create_ad(test_data)

            # Assert
            if case["should_work"]:
                assert response.status_code == 200, f"Valid sellerID case failed: {case['description']}"
                # Cleanup
                ad_id = api_client.extract_ad_id(response.json())
                api_client.delete_ad(ad_id)
            else:
                assert response.status_code == 400, f"BUG: Invalid sellerID was accepted: {case['description']}"

    def test_create_ad_special_characters_in_name(self, api_client, unique_seller_id):
        """Тест специальных символов в названии"""
        special_cases = [
            {"name": "Normal Product Name", "should_work": True},
            {"name": "Product with 'quotes'", "should_work": True},
            {"name": "Product with \"double quotes\"", "should_work": True},
            {"name": "Product with \\backslashes\\", "should_work": True},
            {"name": "Product with <html> tags", "should_work": False},
            {"name": "Product with ${javascript}", "should_work": True},
            {"name": "Product with -- SQL comment", "should_work": True},
            {"name": "Product with ; DROP TABLE", "should_work": True},
        ]

        for case in special_cases:
            # Arrange
            test_data = {
                "sellerID": unique_seller_id,
                "name": case["name"],
                "price": 100,
                "statistics": {
                    "likes": 10,
                    "viewCount": 100,
                    "contacts": 5
                }
            }

            # Act
            response = api_client.create_ad(test_data)

            # Assert
            if case["should_work"]:
                assert response.status_code == 200, f"Valid special chars case failed: {case['name']}"
                # Cleanup
                ad_id = api_client.extract_ad_id(response.json())
                api_client.delete_ad(ad_id)
            else:
                assert response.status_code == 400, f"BUG: Dangerous chars were accepted: {case['name']}"

@pytest.mark.smoke
class TestApiV1Smoke:
    """Smoke-тесты для API v1"""

    def test_smoke_api_connectivity(self, api_client):
        """Smoke-тест: проверка доступности API"""
        # Простой запрос для проверки подключения
        response = api_client.get_ads_by_seller(111111)
        assert response.status_code in [200, 404, 400]  # Любой ответ кроме 5xx

    def test_smoke_create_ad(self, api_client, sample_ad_data):
        """Smoke-тест: создание объявления"""
        response = api_client.create_ad(sample_ad_data)
        assert response.status_code == 200

        # Cleanup
        data = response.json()
        ad_id = api_client.extract_ad_id(data)
        if ad_id:
            api_client.delete_ad(ad_id)