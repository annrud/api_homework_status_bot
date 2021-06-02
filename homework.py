import logging
import os
import time

import requests
import requests.exceptions
from dotenv import load_dotenv
from telegram import Bot

from telegram_log_handler import TelegramLogsHandler

load_dotenv()

PRAKTIKUM_TOKEN = os.getenv('PRAKTIKUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
URL = 'https://praktikum.yandex.ru/api/user_api'
STATUSES_METHOD = 'homework_statuses'


def init_logger(name, tg_bot, chat_id):
    """Инициализация логгера."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('homework.log')
    fh.setLevel(logging.DEBUG)
    th = TelegramLogsHandler(tg_bot, chat_id)
    th.setLevel(logging.ERROR)
    formatter = logging.Formatter(
        '%(asctime)s, [%(levelname)s], %(name)s, '
        '%(message)s, %(filename)s:%(lineno)d'
    )
    fh.setFormatter(formatter)
    th.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(th)
    return logger


bot = Bot(token=TELEGRAM_TOKEN)
logger = init_logger('homework', bot, CHAT_ID)


def parse_homework_status(homework):
    """Парсинг данных JSON: получение статуса домашней работы."""
    homework_name = homework.get('homework_name')
    status = homework.get('status')
    if homework_name is None or status is None:
        raise Exception('В ответе отсутствует один из обязательных ключей: '
                        '"homework_name", "status"')
    verdict = f'У вас проверили работу "{homework_name}".\n\n'
    status_verdict = {
        'reviewing': f'Работа "{homework_name}" взята в ревью.',
        'rejected': f'{verdict}К сожалению в работе нашлись ошибки.',
        'approved': (f'{verdict}Ревьюеру всё понравилось, '
                     'можно приступать к следующему уроку.'),
    }
    if status not in status_verdict.keys():
        raise Exception(f'Отсутствует вердикт для статуса: "{status}"')
    return status_verdict[status]


def get_homework_statuses(current_timestamp):
    """Получение данных JSON от API практикума."""
    if current_timestamp is None:
        current_timestamp = int(time.time())
    headers = {'Authorization': f'OAuth {PRAKTIKUM_TOKEN}'}
    params = {'from_date': current_timestamp}
    url = '/'.join([URL, STATUSES_METHOD, ''])
    try:
        homework_statuses = requests.get(url, headers=headers, params=params)
        return homework_statuses.json()
    except requests.exceptions.RequestException as e:
        logger.error(f'Бот столкнулся с ошибкой: {e}')
        return {}


def send_message(message, bot_client):
    """Отправка сообщения в телеграм."""
    logger.info('Message sending')
    return bot_client.send_message(chat_id=CHAT_ID, text=message)


def main():
    """Запуск телеграм-бота."""
    logger.debug('Bot started')
    current_timestamp = int(time.time())
    while True:
        try:
            new_homework = get_homework_statuses(current_timestamp)
            if new_homework.get('homeworks'):
                send_message(
                    parse_homework_status(new_homework.get('homeworks')[0]),
                    bot
                )
            current_timestamp = new_homework.get(
                'current_date', current_timestamp
            )
            time.sleep(1200)
        except Exception as e:
            logger.error(f'Бот столкнулся с ошибкой: {e}')
            time.sleep(120)


if __name__ == '__main__':
    main()
