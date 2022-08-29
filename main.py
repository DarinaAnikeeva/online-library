import os
import requests
import argparse
import time
from urllib.parse import urljoin, urlsplit

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filepath

def check_for_redirect(response):
    if response.history:
        raise requests.TooManyRedirects


def download_txt(book_name, book_id, folder='books'):
    text_url = f'https://tululu.org/txt.php'
    text_params = {'id': book_id}
    text_response = requests.get(text_url, params=text_params)

    check_for_redirect(text_response)
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f'{book_id}. {book_name}')
    with open(f'{sanitize_filepath(path)}.txt', 'w', encoding='utf-8') as file:
        file.write(text_response.text)


def download_image(book_name, image_link, book_id, folder='images'):
    url_book = urljoin(f'https://tululu.org/b{book_id}', image_link)
    book_response = requests.get(url_book)
    book_response.raise_for_status()
    os.makedirs(folder, exist_ok=True)
    path_to_image = os.path.join(folder,
                                 os.path.split(book_name)[1])
    with open(sanitize_filepath(path_to_image), 'wb') as file:
        file.write(book_response.content)


def parse_book_page(response):
    soup = BeautifulSoup(response.text, 'lxml')
    book_name, author_name = soup.find('table').find('h1').text.split('::')
    image_link = soup.find(class_='bookimage').find('img')['src']

    find_genres = soup.find(class_='d_book').find_all('a')
    book_genres = [genre.text for genre in find_genres]

    find_comments = soup.find_all(class_='texts')
    comments = [comment.find(class_='black').text for comment in find_comments]

    return book_name.strip(), image_link


def starting_download(book_id):
    site_url = f'https://tululu.org/b{book_id}/'
    site_response = requests.get(site_url)
    site_response.raise_for_status()

    book_name, image_link = parse_book_page(site_response)
    download_txt(book_name, book_id)
    download_image(image_link, book_id)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('start_id',
                        nargs='?',
                        default=1,
                        type=int)
    parser.add_argument('end_id',
                        nargs='?',
                        default=11,
                        type=int)
    args = parser.parse_args()

    os.makedirs("books", exist_ok=True)
    os.makedirs("images", exist_ok=True)

    for book_id in range(args.start_id, args.end_id + 1):
        try:
            starting_download(book_id)
        except requests.TooManyRedirects:
            print(f'Книги под номером {book_id} не существует')
        except requests.exceptions.HTTPError as err:
            print(f'При поискe книги номер {book_id} возникла ошибка {err.response.status_code}. ')
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            print('Нет сети, проверьте подключение к интернету ')
            time.sleep(10)

