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


def download_images(book_image, folder='images/'):
    url_book = urljoin('https://tululu.org/', book_image)
    book_response = requests_get(url_book)
    url_book_path = urllib.parse.urlsplit(url_book,
                                          scheme='',
                                          allow_fragments=True)[2]
    path_to_image = os.path.join(folder,
                                 os.path.split(url_book_path)[1])
    with open(path_to_image, 'wb') as file:
        file.write(book_response.content)


def parse_book_page(soup):
    title_tag = soup.find('table').find('h1')
    title_split = title_tag.text.split('::')
    book_name = sanitize_filename(title_split[0].strip())
    author_name = sanitize_filename(title_split[1].strip())
    book_image = soup.find(class_='bookimage').find('img')['src']

    find_genres = soup.find(class_='d_book').find_all('a')
    book_genres = []
    for genre in find_genres:
        book_genres.append(genre.text)

    find_comments = soup.find_all(class_='texts')
    comments = []
    for comment in find_comments:
        comments.append(comment.find(class_='black').text)

    return book_name, author_name, book_image, book_genres, comments


def requests_get(url):
    response = requests.get(url)
    response.raise_for_status()
    return response


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('start_id', nargs='?', default=1, type=int)
    parser.add_argument('end_id', nargs='?', default=11, type=int)
    args = parser.parse_args()

    start_id = args.start_id
    end_id = args.end_id

    os.makedirs("books", exist_ok=True)
    os.makedirs("images", exist_ok=True)

    url = f'https://tululu.org/'
    response = requests_get(url)

    for book_id in range(start_id, end_id + 1):
        site_url = f'{url}b{book_id}/'
        text_url = f'{url}txt.php?id={book_id}'

        site_response = requests_get(site_url)
        text_response = requests_get(text_url)

        if text_response.url != 'https://tululu.org/':
            soup = BeautifulSoup(site_response.text, 'lxml')
            book_name, author_name, book_image, book_genres, comments = parse_book_page(soup)
            download_images(book_image)
            download_txt(book_name, text_response, book_id)
