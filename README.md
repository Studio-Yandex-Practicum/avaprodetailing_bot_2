# Проект Телеграмм-бота 'Avaprodetailing', сделанный командой Антона.

[![Python](https://img.shields.io/badge/Python-blue.svg)](https://www.python.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-blue.svg)](https://www.sqlalchemy.org/)
[![Aiogram](https://img.shields.io/badge/Aiogram-blue.svg)](https://aiogram.readthedocs.io/en/latest/)
[![Alembic](https://img.shields.io/badge/Alembic-blue.svg)](https://alembic.sqlalchemy.org/)

### Стек технологий
* Python==3.11
* aiogram==3.4.1
* SQLAlchemy==2.0.29
* alembic==1.13.1
* pydantic==2.5.3
* qrcode==7.4.2

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

# Деплой на сервер
Запустите docker-compose.yml:
```
cd deploy
docker compose up --build -d
```
Теперь бот должен быть доступен в Telegram по ссылке
```
https://t.me/avaprodetailingbot
```

### Авторы проекта:
- [Антон Земцов](https://github.com/antonata-c)
- [Максим Козлов](https://github.com/mkmmcvrs68)
- [Илья Рыкованов](https://github.com/ilyaryk)
- [Владислав Ермаков](https://github.com/Vladislav199912)
- [Павел Филиппов](https://github.com/pgphil86)
- [Павел Войнов](https://github.com/R1su)
