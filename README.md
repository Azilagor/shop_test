# 🛒 Shop API (FastAPI + PostgreSQL + Alembic)

Описание
Тестовый проект интернет-магазина на FastAPI.  
Реализовано:
- Категории (с деревом вложенности)
- Продукты
- Клиенты
- Заказы
- Добавление товаров в заказ с проверкой склада

База данных — PostgreSQL, миграции через Alembic.  
Документация API доступна через Swagger (`/docs`).


1. Клонирование проекта
```bash
git clone https://github.com/Azilagor/shop_test.git
cd shop_test

2. Создание виртуального окружения
python3 -m venv venv
source venv/bin/activate

3. Установка зависимостей
pip install -r requirements.txt


4. Запуск API
uvicorn main:app --reload

API будет доступен по адресу:
 http://127.0.0.1:8000/docs

Запуск через Docker
1. Сборка контейнера
docker-compose up --build


2. Применение миграций
docker-compose exec api alembic upgrade head
