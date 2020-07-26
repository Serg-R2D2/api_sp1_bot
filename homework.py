import os
import requests
import telegram
import time
import logging
from dotenv import load_dotenv

load_dotenv()


PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

proxy_url='socks5://54.179.53.101:80'
ya_p_url = 'https://praktikum.yandex.ru/api/user_api/homework_statuses/'


def parse_homework_status(homework):
    homework_name = homework["homework_name"]
    if homework["status"] == 'rejected':
        verdict = 'К сожалению в работе нашлись ошибки.'
    else:
        verdict = 'Ревьюеру всё понравилось, можно приступать к следующему уроку.'
    return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'


def get_homework_statuses(current_timestamp):
    headers = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}
    data = {'from_date': current_timestamp}
    try:
        homework_statuses = requests.get(ya_p_url, params=data, headers=headers)
    except Exception as e:
        logging.error(f'Error: {e}')
        raise e
    return homework_statuses.json()


def send_message(message):
    proxy = telegram.utils.request.Request(proxy_url=proxy_url)
    bot = telegram.Bot(token=TELEGRAM_TOKEN, request=proxy)
    return bot.send_message(chat_id=CHAT_ID, text=message)


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
            else:
                print('Ничего нового')
            current_timestamp = new_homework.get('current_date')  # обновить timestamp
            if current_timestamp == None:
                current_timestamp = int(time.time())
            time.sleep(10)  # опрашивать раз в двадцать минут

        except Exception as e:
            print(f'Бот упал с ошибкой: {e}')
            time.sleep(5)
            continue


if __name__ == '__main__':
    main()
