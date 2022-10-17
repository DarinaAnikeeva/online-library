import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from livereload import Server
from jinja2 import Environment, FileSystemLoader, select_autoescape
from more_itertools import chunked

def on_reload():
    with open("books_params.json", 'r', encoding='utf-8') as file:
        books_params = file.read()
        params_dicts = json.loads(books_params)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    book_params = list(chunked(params_dicts, 2))
    rendered_page = template.render(
        books_params=book_params,
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

on_reload()

server = Server()
server.watch('template.html', on_reload)
server.serve(root='.')


