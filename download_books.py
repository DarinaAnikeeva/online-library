import os
import requests
import json
import time
import argparse

from parse_page import parse_book_page
from parse_tululu_category import parse_category_page
from urllib.parse import urljoin
from pathvalidate import sanitize_filepath

def check_for_redirect(response):
    if response.history:
        raise requests.TooManyRedirects

def download_txt(book_name, book_id, folder='books'):
    text_url = f'https://tululu.org/txt.php'
    text_params = {'id': book_id}
    text_response = requests.get(text_url, params=text_params)

    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f'{book_name}')
    with open(f'{sanitize_filepath(path)}.json', 'w', encoding='UTF-8') as json_file:
        json.dump(text_response.text, json_file, ensure_ascii=False)

def download_image(book_name, image_link, url, folder='books'):
    url_book = urljoin(url, image_link)
    book_response = requests.get(url_book)
    book_response.raise_for_status()
    os.makedirs(folder, exist_ok=True)
    path_to_image = os.path.join(folder,
                                 os.path.split(book_name)[1])
    with open(f'{sanitize_filepath(path_to_image)}.jpg', 'wb') as file:
        file.write(book_response.content)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--start_id',
                        nargs='?',
                        default=1,
                        type=int)
    parser.add_argument('--end_id',
                        nargs='?',
                        default=701,
                        type=int)
    parser.add_argument('--skip_imgs',
                        nargs='?',
                        help='не скачивать картинки',
                        type=bool,
                        default=False)
    parser.add_argument('--skip_txt',
                        nargs='?',
                        help='не скачивать книги',
                        type=bool,
                        default=False)

    args = parser.parse_args()

    choise = int(input('''Напишите
        1 - если вы хотите скачать книги диапозоном
        2 - если вы хотите скачать книги по номерам
        3 - если вы хотите скачать книги с категории
        : '''))
    if choise == 1:
        books_range_input = input(
            'Введите номера книги c которой начать и которой закончить скачивание через запятую: ')
        start, stop = books_range_input.split(',')
        books_range = [book for book in range(int(start), int(stop) + 1)]
    elif choise == 2:
        numbers = input('Введите номера желаемых книг для скачивания через запятую: ')
        books_range = numbers.split(',')
    elif choise == 3:
        category_url = input('''Введите url адрес сайта с категорией. Пример - https://tululu.org/l55/
                : ''')
        start_page = int(input('Введите номер страницы, с которой начать скачивание: '))
        finish_page = int(input('Введите номер страницы, которой закончить скачивание: '))
        print('Загружаем книги с выбранной категории. Подождите.')
        books_range = []
        for number in range(start_page, finish_page + 1):
            try:
                response = requests.get(f'{category_url}{number}/')
                response.raise_for_status()
                check_for_redirect(response)

                books_id = parse_category_page(response)
                books_range.extend(books_id)
            except requests.TooManyRedirects:
                print(f'Oops. Книги под номером {number} не существует')
            except requests.exceptions.HTTPError as err:
                code = err.response.status_code
                print(f'Oops. При поиски книги номер {number} возникла ошибка {code}')
                print(f'Response is: {err.response.content}')
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                print('Oops. Ошибка соединения. Проверьте интернет связь')
                time.sleep(20)
    else:
        print('Неверно введена цифра')

    books_params = []
    for number in books_range:
        try:
            url = f'https://tululu.org/b{number}/'
            response = requests.get(url)
            response.raise_for_status()
            check_for_redirect(response)

            book_name, author_name, image_link, book_genres, comments = parse_book_page(response)
            book_params = {
                'title': book_name,
                'author': author_name,
                'img_srс': os.path.join('books', f'{book_name}.jpg'),
                'book_path': os.path.join('books', f'{book_name}.json'),
                'comments': comments,
                'genres': book_genres
            }
            books_params.append(book_params)

            if not args.skip_imgs:
                download_image(book_name, image_link, url)

            if not args.skip_txt:
                download_txt(book_name, number)
        except requests.TooManyRedirects:
            print(f'Книги под номером {id} не существует')
        except requests.exceptions.HTTPError as err:
            print(f'При поискe книги номер {id} возникла ошибка {err.response.status_code}. ')
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            print('Нет сети, проверьте подключение к интернету ')
            time.sleep(10)

    with open('books_params.json', 'w', encoding='utf8') as json_file:
        json.dump(books_params, json_file, ensure_ascii=False)
