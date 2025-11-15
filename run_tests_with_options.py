#!/usr/bin/env python3
"""
Расширенный скрипт для запуска тестов с различными опциями
"""

import subprocess
import sys
import argparse
from pathlib import Path


def run_pytest_command(command):
    """Запускает команду pytest и возвращает результат"""
    print(f"Выполняется: {' '.join(command)}")
    print("=" * 80)

    result = subprocess.run(command)
    print("=" * 80)
    return result.returncode


def main():
    parser = argparse.ArgumentParser(description='Запуск тестов API v1 и v2')
    parser.add_argument('--smoke', action='store_true', help='Запустить только smoke-тесты')
    parser.add_argument('--v1-only', action='store_true', help='Запустить только тесты API v1')
    parser.add_argument('--v2-only', action='store_true', help='Запустить только тесты API v2')
    parser.add_argument('--negative', action='store_true', help='Запустить только негативные тесты')
    parser.add_argument('--security', action='store_true', help='Запустить только security тесты')
    parser.add_argument('--verbose', '-v', action='store_true', help='Подробный вывод')
    parser.add_argument('--html-report', action='store_true', help='Сгенерировать HTML отчет')

    args = parser.parse_args()

    # Базовые файлы тестов
    test_files = []
    if args.v1_only:
        test_files = ["test_api_v1.py"]
    elif args.v2_only:
        test_files = ["test_api_v2.py"]
    else:
        test_files = ["test_api_v1.py", "test_api_v2.py"]

    # Проверяем существование файлов
    missing_files = [f for f in test_files if not Path(f).exists()]
    if missing_files:
        print(f"Ошибка: Не найдены файлы тестов: {missing_files}")
        sys.exit(1)

    # Формируем команду pytest
    command = [sys.executable, "-m", "pytest"]
    command.extend(test_files)

    # Добавляем маркеры
    markers = []
    if args.smoke:
        markers.append("smoke")
    if args.negative:
        markers.append("TestApiV1Negative or TestApiV2Negative")
    if args.security:
        markers.append("TestApiV1Security")

    if markers:
        command.extend(["-m", " and ".join(markers)])

    # Добавляем опции вывода
    if args.verbose:
        command.append("-v")

    command.extend(["--tb=short", "--color=yes"])

    # HTML отчет
    if args.html_report:
        command.extend(["--html=test_report.html", "--self-contained-html"])

    # Запускаем тесты
    return_code = run_pytest_command(command)

    # Вывод результата
    if return_code == 0:
        print("✅ Все тесты прошли успешно!")
    else:
        print("❌ Некоторые тесты завершились с ошибками")

    sys.exit(return_code)


if __name__ == "__main__":
    main()