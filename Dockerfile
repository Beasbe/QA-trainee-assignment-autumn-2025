FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x run_tests.sh

# Используем sh вместо bash
CMD ["/bin/sh", "-c", "./run_tests.sh"]