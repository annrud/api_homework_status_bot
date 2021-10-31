# api_homework_status_bot

*Бот-ассистент api_homework_status_bot обращается к API сервиса Практикум.Домашка и отправляет уведомление в мессенджер Telegram со статусом проверки домашней работы ревьюером, логирует свою работу и сообщает о важных проблемах сообщением в Telegram.<br/>
Статусы домашней работы:<br>
reviewing: работа взята в ревью;
approved: ревью успешно пройдено;
rejected: в работе есть ошибки, нужно поправить.*

## Технологии:<br>
api_homework_status_bot реализован с применением библиотеки python-telegram-bot для работы с Telegram Bot API.


1. Склонируйте репозиторий в свою рабочую директорию:<br>
```git clone https://github.com/annrud/api_homework_status_bot.git```
2. Создайте и активируйте виртуальное окружение:<br>
```python -m venv venv```<br>
```source venv/bin/activate```

2. Установите зависимости:<br>
```pip install -r requirements.txt```

4. Cоздайте файл .env с переменными окружения 'PRAKTIKUM_TOKEN', 'TELEGRAM_TOKEN', 'TELEGRAM_CHAT_ID'.
   
  - Получите 'PRAKTIKUM_TOKEN':<br>
    https://oauth.yandex.ru/authorize?response_type=token&client_id=1d0b9dd4d652455a9eb710d450ff456a
  - Зарегистрируйте бота в Telegram (используйте @BotFather), получите 'TELEGRAM_TOKEN' и ID своего Telegram-аккаунта 'TELEGRAM_CHAT_ID'.
7. Запуск бота:<br>
```python homework.py```