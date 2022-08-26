import os
import requests
import urllib
import argparse

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin


def download_txt(book_name, text_response, book_id, folder='books/'):
    with open(f'{folder}{book_id}. {book_name}.txt', 'w', encoding='utf-8') as file:
        file.write(text_response.text)


def download_image(image_link, folder='images/'):
    url_book = urljoin('https://tululu.org/', image_link)
    book_response = requests.get(url_book)
    url_book_path = urllib.parse.urlsplit(url_book,
                                          scheme='',
                                          allow_fragments=True)[2]
    path_to_image = os.path.join(folder,
                                 os.path.split(url_book_path)[1])
    with open(path_to_image, 'wb') as file:
        file.write(book_response.content)


def parse_book_page(response, number):
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find('table').find('h1')
    title_split = title_tag.text.split('::')
    book_name = sanitize_filename(title_split[0].strip())
    author_name = sanitize_filename(title_split[1].strip())
    print(number, 'Название: ', book_name, 'Автор: ', author_name )

    find_genres = soup.find(class_='d_book').find_all('a')
    book_genres = []
    for genre in find_genres:
        book_genres.append(genre.text)
    print("Жанры: ", book_genres)

    find_comments = soup.find_all(class_='texts')
    print("Комментарии: ")
    for comment in find_comments:
        print(comment.find(class_='black').text)
    print()



def parse_tululu(start_id, end_id):
    for book_id in range(start_id, end_id + 1):
        site_url = f'https://tululu.org/b{book_id}/'
        text_url = f'https://tululu.org/txt.php?id={book_id}'

        site_response = requests.get(site_url)
        text_response = requests.get(text_url)

        if text_response.url != 'https://tululu.org/':
            parse_book_page(site_response, book_id)

    download_books()


def download_books():
    numbers = input('Введите номера книг через запятую: ')
    for number in numbers.split(','):
        site_url = f'https://tululu.org/b{number.strip()}/'
        text_url = f'https://tululu.org/txt.php?id={number.strip()}'
        site_response = requests.get(site_url)
        text_response = requests.get(text_url)

        soup = BeautifulSoup(site_response.text, 'lxml')
        title_tag = soup.find('table').find('h1')
        book_name = title_tag.text.split('::')[0].strip()
        image_link = soup.find(class_='bookimage').find('img')['src']

        download_image(image_link)
        download_txt(book_name, text_response, number.strip())


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

    start_id = args.start_id
    end_id = args.end_id

    os.makedirs("books", exist_ok=True)
    os.makedirs("images", exist_ok=True)

    parse_tululu(start_id, end_id)