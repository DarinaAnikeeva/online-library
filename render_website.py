import json
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from livereload import Server
from jinja2 import Environment, FileSystemLoader, select_autoescape
from more_itertools import chunked

def on_reload():
    with open("books_params.json", 'r', encoding='utf-8') as file:
        params_dicts = json.load(file)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    os.makedirs('pages',  exist_ok=True)
    quantity_books_in_page = 15
    books_pages = list(chunked(params_dicts, quantity_books_in_page))

    for number, books_page in enumerate(books_pages, start=1):
        quantity_books_in_raw = 2
        books_params = list(chunked(books_page, quantity_books_in_raw))
        rendered_page = template.render(
            books_params=books_params,
            books_pages=len(books_pages),
            page_number=number
        )

        with open(f'pages\index{number}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)

if __name__ == '__main__':
    on_reload()

    server = Server()
    server.watch('template.html', on_reload)
    server.watch('books_params.json', on_reload)
    server.serve(root='.')


