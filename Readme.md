# API Tests

Автоматические тесты для QA-trainee-assignment-autumn-2025

## Быстрый старт


### Запуск тестов

1. **Собрать и запустить все тесты:**
   ```bash
   docker-compose build
   docker-compose run api-tests ./run_tests.sh
   ```
2. **Запуск тестов напрямую (без Docker):**
   ```bash
   # Установить зависимости Python
   pip install -r requirements.txt
   
   # Запустить тесты
   ./run_tests.sh
   ```
3. Запуск отдельных групп тестов:

   ```bash
   # Только позитивные тесты
   pytest -m positive
   
   # Только негативные тесты  
   pytest -m negative
   
   # Только security тесты
   pytest -m security
   
   # Только smoke тесты
   pytest -m smoke
   ```
4. Запуск с отчетом:

   ```bash
   pytest --html=report.html --self-contained-html
   ```