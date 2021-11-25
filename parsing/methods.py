import requests


def telegram_info(crawl):
    requests.request(
        'GET',
        url=f'https://api.telegram.org/bot1415683360:AAGdNPshUmpR_-KQRdwITa6TyfB4tIAxJdw/sendMessage?chat_id='
            f'-1001177590173&text=Парсинг {crawl} завершен'
    )