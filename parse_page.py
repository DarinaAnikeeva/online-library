from bs4 import BeautifulSoup


def parse_book_page(response):
    soup = BeautifulSoup(response.text, 'lxml')
    book_name, author_name = soup.select('table h1')[0].text.split('::')
    title_name = book_name.replace('.', '!')
    image_link = soup.select('.bookimage img')[0]['src']

    book_genres = soup.select('span.d_book a')
    genres = [genre.text for genre in book_genres]

    find_comments = soup.select('texts .black')
    comments = [comment.text for comment in find_comments]

    return title_name.strip(), author_name, image_link, genres, comments


