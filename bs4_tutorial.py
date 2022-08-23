import requests
from bs4 import BeautifulSoup

url = 'https://www.franksonnenbergonline.com/blog/finding-the-right-answer-begins-with-the-right-question/'
response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'lxml')
title_tag = soup.find('main').find('header').find('h1')
title_text = title_tag.text
print(title_text)