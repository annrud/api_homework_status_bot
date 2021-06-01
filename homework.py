import logging
import os
import time

import requests
from dotenv import load_dotenv
from telegram import Bot

from telegram_log_handler import TelegramLogsHandler

load_dotenv()


def init_logger(name, tg_bot, chat_id):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('homework.log')
    fh.setLevel(logging.DEBUG)
    th = TelegramLogsHandler(tg_bot, chat_id)
    th.setLevel(logging.ERROR)
    formatter = logging.Formatter(
        '%(asctime)s, [%(levelname)s], %(name)s, %(message)s, %(filename)s'
    )
    fh.setFormatter(formatter)
    th.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(th)
    return logger


PRAKTIKUM_TOKEN = os.getenv('PRAKTIKUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
url = 'https://praktikum.yandex.ru/api/user_api/homework_statuses/'
bot = Bot(token=TELEGRAM_TOKEN)
logger = init_logger('homework', bot, CHAT_ID)


def parse_homework_status(homework):
    homework_name = homework["homework_name"]
    status = homework["status"]
    if status == 'reviewing':
        return f'Работа "{homework_name}" взята в ревью.'
    if status == 'rejected':
        verdict = 'К сожалению в работе нашлись ошибки.'
    elif status == 'approved':
        verdict = ('Ревьюеру всё понравилось, '
                   'можно приступать к следующему уроку.')
    return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'


def get_homework_statuses(current_timestamp):
    if current_timestamp is None:
        current_timestamp = 0
    headers = {'Authorization': f'OAuth {PRAKTIKUM_TOKEN}'}
    params = {'from_date': current_timestamp}
    homework_statuses = requests.get(url, headers=headers, params=params)
    return homework_statuses.json()


def send_message(message, bot_client):
    logger.info('Message sending')
    return bot_client.send_message(chat_id=CHAT_ID, text=message)


def main():
    logger.debug('Bot started')
    current_timestamp = 0
    while True:
        try:
            new_homework = get_homework_statuses(current_timestamp)
            if new_homework.get('homeworks'):
                send_message(
                    parse_homework_status(new_homework.get('homeworks')[0]),
                    bot
                )
            current_timestamp = new_homework.get(
                'current_date', int(time.time())
            )
            time.sleep(300)
        except Exception as e:
            logger.error(f'Бот столкнулся с ошибкой: {e}')
            time.sleep(120)


if __name__ == '__main__':
    main()
