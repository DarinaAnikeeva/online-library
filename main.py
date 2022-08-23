import os
import requests


os.makedirs("books", exist_ok=True)


for book_id in range(1,11):
    url1 = f'https://tululu.org/txt.php?id={book_id}'
    response = requests.get(url1)
    response.raise_for_status()
    if response.url != 'https://tululu.org/':
        with open(f'books/id{book_id}.txt', 'w') as file:
            file.write(response.text)

