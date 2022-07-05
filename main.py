import argparse
import os
import requests

from urllib.parse import urlparse
from dotenv import load_dotenv



def is_bitlink(token, url):
    parsed_url = urlparse(url)
    bitlink = f'{parsed_url.netloc}{parsed_url.path}'
    api_endpoint = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}'

    headers = {
        'Authorization': token,
    }

    response = requests.get(
        url=api_endpoint,
        headers=headers,
    )
    return response.ok


def shorten_link(token, url):
    api_endpoint = 'https://api-ssl.bitly.com/v4/bitlinks'

    headers = {
        'Authorization': token,
    }

    payload = {
        'long_url': url,
    }

    response = requests.post(
        url=api_endpoint,
        headers=headers,
        json=payload,
    )
    response.raise_for_status()
    return response.json().get('link')


def count_clicks(token, link):
    parsed_link = urlparse(link)
    bitlink = f'{parsed_link.netloc}{parsed_link.path}'
    api_endpoint = (
        f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
    )

    headers = {
        'Authorization': token,
    }

    response = requests.get(
        url=api_endpoint,
        headers=headers,
    )
    response.raise_for_status()
    return response.json().get('total_clicks')


def main():
    load_dotenv()
    bitly_api_token = os.getenv('BITLY_API_TOKEN')

    parser = argparse.ArgumentParser()
    parser.add_argument('link', help='bitlink or target link')
    args = parser.parse_args()

    try:
        if is_bitlink(bitly_api_token, args.link):
            total_clicks = count_clicks(bitly_api_token, args.link)
            print(f'Сумма кликов по ссылке: {total_clicks}')
        else:
            bitlink = shorten_link(bitly_api_token, args.link)
            print(bitlink)
    except requests.exceptions.HTTPError:
        print('Введен некорректный адрес')


if __name__ == '__main__':
    main()
