#!/bin/bash
#
# Скрипт для запуска тестов в Docker
#

# Цвета для вывода
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}Запуск API тестов в Docker${NC}"

# Функция для вывода помощи
show_help() {
    echo "Использование: $0 [команда]"
    echo ""
    echo "Команды:"
    echo "  build     - Собрать Docker образ"
    echo "  run       - Запустить тесты в Docker"
    echo "  dev       - Запустить интерактивный контейнер для разработки"
    echo "  stop      - Остановить контейнер"
    echo "  clean     - Остановить и удалить контейнер"
    echo "  reports   - Показать отчеты тестов"
    echo "  help      - Показать эту справку"
    echo ""
    echo "Пример: $0 run"
}

# Функция для сборки образа
build_image() {
    echo -e "${BLUE}Сборка Docker образа...${NC}"
    docker build -t api-tests .
}

# Функция для запуска тестов
run_tests() {
    echo -e "${BLUE}Запуск тестов в Docker...${NC}"

    # Собираем образ если нужно
    if [[ "$(docker images -q api-tests 2> /dev/null)" == "" ]]; then
        build_image
    fi

    # Запускаем тесты
    docker run -it --rm \
        --name api-tests-runner \
        -v $(pwd)/reports:/app/reports \
        api-tests
}

# Функция для разработки
run_dev() {
    echo -e "${BLUE}Запуск интерактивного контейнера для разработки...${NC}"

    # Собираем dev образ
    docker build -t api-tests-dev -f Dockerfile.dev .

    # Запускаем интерактивный контейнер
    docker run -it --rm \
        --name api-tests-dev \
        -v $(pwd):/app \
        -v $(pwd)/reports:/app/reports \
        -v $(pwd)/logs:/app/logs \
        api-tests-dev
}

# Функция для остановки
stop_container() {
    echo -e "${BLUE}Остановка контейнера...${NC}"
    docker stop api-tests-runner 2>/dev/null || true
    docker stop api-tests-dev 2>/dev/null || true
}

# Функция для очистки
clean_container() {
    echo -e "${BLUE}Очистка контейнеров...${NC}"
    docker rm -f api-tests-runner 2>/dev/null || true
    docker rm -f api-tests-dev 2>/dev/null || true
}

# Функция для показа отчетов
show_reports() {
    echo -e "${BLUE}Отчеты тестов:${NC}"
    if [ -d "reports" ]; then
        find reports/ -type f -name "*.html" -o -name "*.xml" -o -name "*.json" | while read file; do
            echo "  $file"
        done
    else
        echo "  Директория reports не найдена"
    fi
}

# Обработка команд
case "${1:-help}" in
    "build")
        build_image
        ;;
    "run")
        run_tests
        ;;
    "dev")
        run_dev
        ;;
    "stop")
        stop_container
        ;;
    "clean")
        clean_container
        ;;
    "reports")
        show_reports
        ;;
    "help"|"-h"|"--help")
        show_help
        ;;
    *)
        echo -e "${RED}Неизвестная команда: $1${NC}"
        show_help
        exit 1
        ;;
esac