#!/bin/bash
#
# Скрипт для запуска тестов API с привязкой к классам
#

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Функции для вывода
print_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }
print_menu() { echo -e "${CYAN}$1${NC}"; }

# Проверка файлов тестов
check_test_files() {
    if [[ ! -f "test_api_v1.py" ]]; then
        print_error "Файл test_api_v1.py не найден!"
        return 1
    fi
    if [[ ! -f "test_api_v2.py" ]]; then
        print_error "Файл test_api_v2.py не найден!"
        return 1
    fi
    return 0
}

# Функция для запуска тестов
run_tests() {
    local command=$1
    local description=$2

    print_info "Запуск: $description"
    echo "================================================"

    eval $command

    local result=$?
    echo "================================================"

    if [ $result -eq 0 ]; then
        print_success "Тесты завершены успешно!"
    else
        print_error "Тесты завершены с ошибками!"
    fi

    return $result
}

# Функция для паузы
pause() {
    echo ""
    print_info "Нажмите любую клавишу для продолжения..."
    read -n 1 -s
}

# Основное меню
main() {
    # Проверяем файлы тестов
    if ! check_test_files; then
        pause
        exit 1
    fi

    while true; do
        clear
        echo "================================================"
        print_menu "           🚀 ТЕСТИРОВАНИЕ API"
        echo "================================================"
        echo ""
        print_menu "=== API V1 ==="
        echo "1.  TestApiV1Positive - Позитивные тесты"
        echo "2.  TestApiV1Negative - Негативные тесты"
        echo "3.  TestApiV1Integration - Интеграционные тесты"
        echo "4.  TestApiV1Security - Security тесты"
        echo "5.  TestApiV1Smoke - Smoke тесты"
        echo ""
        print_menu "=== API V2 ==="
        echo "6.  TestApiV2Positive - Позитивные тесты"
        echo "7.  TestApiV2Negative - Негативные тесты"
        echo "8.  TestApiV2Integration - Интеграционные тесты"
        echo "9.  TestApiV2Smoke - Smoke тесты"
        echo ""
        print_menu "=== ГРУППЫ ==="
        echo "10. Все тесты API v1"
        echo "11. Все тесты API v2"
        echo "12. Все тесты (v1 + v2)"
        echo "13. Все Smoke тесты"
        echo "14. Все Negative тесты"
        echo "15. Все Integration тесты"
        echo "0.  Выход"
        echo ""
        echo "================================================"
        read -p "Выберите опцию (0-15): " choice

        case $choice in
            # API V1
            1)
                run_tests "python -m pytest test_api_v1.py -k \"TestApiV1Positive\" -v --tb=short" "TestApiV1Positive - Позитивные тесты v1"
                ;;
            2)
                run_tests "python -m pytest test_api_v1.py -k \"TestApiV1Negative\" -v --tb=short" "TestApiV1Negative - Негативные тесты v1"
                ;;
            3)
                run_tests "python -m pytest test_api_v1.py -k \"TestApiV1Integration\" -v --tb=short" "TestApiV1Integration - Интеграционные тесты v1"
                ;;
            4)
                run_tests "python -m pytest test_api_v1.py -k \"TestApiV1Security\" -v --tb=short" "TestApiV1Security - Security тесты v1"
                ;;
            5)
                run_tests "python -m pytest test_api_v1.py -k \"TestApiV1Smoke\" -v --tb=short" "TestApiV1Smoke - Smoke тесты v1"
                ;;
            # API V2
            6)
                run_tests "python -m pytest test_api_v2.py -k \"TestApiV2Positive\" -v --tb=short" "TestApiV2Positive - Позитивные тесты v2"
                ;;
            7)
                run_tests "python -m pytest test_api_v2.py -k \"TestApiV2Negative\" -v --tb=short" "TestApiV2Negative - Негативные тесты v2"
                ;;
            8)
                run_tests "python -m pytest test_api_v2.py -k \"TestApiV2Integration\" -v --tb=short" "TestApiV2Integration - Интеграционные тесты v2"
                ;;
            9)
                run_tests "python -m pytest test_api_v2.py -k \"TestApiV2Smoke\" -v --tb=short" "TestApiV2Smoke - Smoke тесты v2"
                ;;
            # ГРУППЫ
            10)
                run_tests "python -m pytest test_api_v1.py -v --tb=short" "Все тесты API v1"
                ;;
            11)
                run_tests "python -m pytest test_api_v2.py -v --tb=short" "Все тесты API v2"
                ;;
            12)
                run_tests "python -m pytest test_api_v1.py test_api_v2.py -v --tb=short" "Все тесты (v1 + v2)"
                ;;
            13)
                run_tests "python -m pytest test_api_v1.py test_api_v2.py -k \"TestApiV1Smoke or TestApiV2Smoke\" -v --tb=short" "Все Smoke тесты"
                ;;
            14)
                run_tests "python -m pytest test_api_v1.py test_api_v2.py -k \"TestApiV1Negative or TestApiV2Negative\" -v --tb=short" "Все Negative тесты"
                ;;
            15)
                run_tests "python -m pytest test_api_v1.py test_api_v2.py -k \"TestApiV1Integration or TestApiV2Integration\" -v --tb=short" "Все Integration тесты"
                ;;
            0)
                print_info "Выход из программы..."
                exit 0
                ;;
            *)
                print_error "Неверный выбор. Попробуйте снова."
                ;;
        esac

        pause
    done
}

# Запускаем скрипт
main