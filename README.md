Telegram Shop Bot 🛒
Учебный проект на Python с использованием Aiogram, Docker и PostgreSQL.

🎯 Цели проекта
Научиться работать с Aiogram: настройка бота, обработчики, state machine

Изучить работу с PostgreSQL через asyncpg

Освоить Docker: создание образов, переменные окружения, запуск приложений


🚀 Начало работы Установка и запуск 

Клонируйте репозиторий:

    git clone https://github.com/AydenRU/tg_shop_bot.git

    cd tg_shop_bot

Создайте файл .env в корне:

dotenv

    TOKEN=ваш_токен_бота

    HOST=host.docker.internal  # если PostgreSQL локально

    DATABASE=AydenShopBot
    
    USER=postgres

    PASSWORD=postgres

Запустите контейнер:

    docker run --env-file .env -p 8000:8000 имя_imeg

🧩 Технологии

Python 3.13 — основной язык проекта

Aiogram — асинхронная библиотека для Telegram-ботов

asyncpg — асинхронная библиотека для PostgreSQL

PostgreSQL — база данных

Docker — контейнеризация приложения

🛠 Функционал
Регистрация пользователя и авторизация через Telegram

Каталог товаров с возможностью просмотра и добавления в корзину

Оформление заказа пользователем

Взаимодействие с базой данных для хранения товаров, заказов и пользователей

