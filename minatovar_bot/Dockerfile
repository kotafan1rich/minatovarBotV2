FROM python:3.9
RUN mkdir /app

WORKDIR /app

COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Копируем исходный код бота в контейнер
COPY . .
# Команда для запуска бота
CMD ["python", "src/main.py"]