import re

from bs4 import BeautifulSoup


def parse_category_page(response):
    soup = BeautifulSoup(response.text, 'lxml')
    books = soup.select('.ow_px_td .bookimage a')
    books_id = []
    for book in books:
        book_id = int(re.findall(r'-?\d+\.?\d*', book['href'])[0])
        books_id.append(book_id)
    return books_id

