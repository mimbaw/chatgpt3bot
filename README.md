# test_task

Этот бот предназначен для использования ChatGPT в телеграмм.

Команды:
    /clear_dialog - Нужна для того, чтобы сбросить контекст диалога
____

Как пользоваться:
    Просто запустите бота, и общайтесь с ним, как с человеком. Помните, что существуют ограничение на количество запросов(не более 3 в минуту), а также на размер самого запроса(не более 4000 токенов)
    В файле backend\data.json сохраняется история общения пользователя с нейросетью.
____  

Инструкция по установке:
1. Используйте python версии 3 и выше;
2. Перейдите в директорию проекта;
3. Далее настройте виртуальное окружение:
    1. Создаем виртуальное окружение командой - python3 -m venv venv
    + Для windows:
       + Переходим в виртальное окружение командой - venv/Scripts/activate
    + Для linux:
       + Переходим в виртальное окружение командой - source venv/bin/activate
    3. Устанавливаем библиотеки командой - python3 -m pip install -r requirements.txt
4. Заполняем необходимые поля в файле config.py
5. Запускаем бота - python3 main.py

Для сервером испольуем менеджер процессов pm2 или подобные
