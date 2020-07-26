import os
import requests
import telegram
import time
import logging
from dotenv import load_dotenv

load_dotenv()


PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
<<<<<<< HEAD
<<<<<<< HEAD
CHAT_ID = os.getenv('CHAT_ID')
print(CHAT_ID)
=======
CHAT_ID = '1131227628'
>>>>>>> a21d7c7e032b564e6905b67329039fdcd7316f83
=======
CHAT_ID = os.getenv('CHAT_ID')
>>>>>>> ecdbe12e6befab5d4cdaed2696cc19ae81d5725e

YA_PRACTIKUM_URL = 'https://praktikum.yandex.ru/api/user_api/homework_statuses/'
BOT = telegram.Bot(token=TELEGRAM_TOKEN)


def parse_homework_status(homework):
    everything_ok = (
        homework['homework_name'] is not None 
        and homework['status'] is not None 
        and homework['status'] == 'rejected' or homework['status'] == 'approved'
        )
    if not everything_ok:
        send_message('Неверный ответ сервера')
    homework_name = homework["homework_name"]
    if homework["status"] == 'rejected':
        verdict = 'К сожалению в работе нашлись ошибки.'
    else:
        verdict = 'Ревьюеру всё понравилось, можно приступать к следующему уроку.'
    return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'


def get_homework_statuses(current_timestamp):
    if current_timestamp is None:
        current_timestamp = int(time.time())
    headers = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}
    data = {'from_date': current_timestamp}
    try:
        homework_statuses = requests.get(
            YA_PRACTIKUM_URL, 
            params=data, 
            headers=headers
        )
    except requests.exceptions.RequestException as e:
        logging.error(f'Error: {e}')
        raise {}
    return homework_statuses.json()


def send_message(message): 
    return BOT.send_message(chat_id=CHAT_ID, text=message) 

def main():
    current_timestamp = int(time.time())  # начальное значение timestamp
    while True:
        try:
            new_homework = get_homework_statuses(current_timestamp)
            if new_homework.get('homeworks'):
                send_message(
                    parse_homework_status(
                        new_homework.get('homeworks')[0])
                )
            current_timestamp = new_homework.get('current_date')  # обновить timestamp
            time.sleep(660)  # опрашивать раз в 11 минут
        except Exception as e:
            print(f'Бот упал с ошибкой: {e}')
            time.sleep(10)
            continue


if __name__ == '__main__':
    main()
