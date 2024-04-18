# Проект Телеграмм-бота 'Avaprodetailing', сделанный командой Антона.

[![Python](https://img.shields.io/badge/Python-blue.svg)](https://www.python.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-blue.svg)](https://www.sqlalchemy.org/)
[![Aiogram](https://img.shields.io/badge/Aiogram-blue.svg)](https://aiogram.readthedocs.io/en/latest/)
[![Alembic](https://img.shields.io/badge/Alembic-blue.svg)](https://alembic.sqlalchemy.org/)

### Над проектом работают:
- https://github.com/antonata-c
- https://github.com/mkmmcvrs68
- https://github.com/ilyaryk
- https://github.com/Vladislav199912
- https://github.com/pgphil86
- https://github.com/R1su

### Описание:
Avaprodetailing - это Telegram-бот, разработанный для автосервиса, который предоставляет комплексную систему лояльности для клиентов. Бот позволяет клиентам:
1. Регистрироваться в программе лояльности,
1. Зарабатывать баллы за посещения и услуги,
1. Обменивать баллы на скидки и бесплатные услуги,
1. Отслеживать историю своих посещений и баланс баллов,
1. Получать персональные предложения и уведомления.

### Работа с проектом.
Для начала необходимо клонировать репозиторий и зайти в рабочую директорию проекта.
```
git@github.com:Studio-Yandex-Practicum/avaprodetailing_bot_2.git
```
```
cd avaprodetailing_bot_2
```
Далее создаем и активируем виртуальное окружение.
```
python3 -m venv venv
```
```
source venv/bin/activate
```
После устанавливаем зависимости из requirements.txt.
```
python3 -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
В корневой директории проекта создаем файл .env с переменными:
```
BOT_TOKEN = 'Ваш токен'
DATABASE_URL = sqlite+aiosqlite:///./avapro.db
```
Примените миграцию, выполнив команду:
```
alembic upgrade head
```
Запустите бота с помощью команды:
```
python main.py
```

# Деплой на сервер ???????????
Постройте Docker-образ:
```
docker build -t avaprodetailing .
```
Запустите контейнер:
```
docker run -p 80:80 avaprodetailing
```
Теперь бот должен быть доступен по адресу.
```
http://localhost:80
```

### В проекте используются:
1. Python==3.11
1. aiogram==3.4.1
1. SQLAlchemy==2.0.29
1. alembic==1.13.1
1. pydantic==2.5.3
1. qrcode==7.4.2
