import random
import requests
from bs4 import BeautifulSoup


class DataManager:
    def __init__(self):
        random_page_num = random.randint(1, 100)
        URL = f'https://www.goodreads.com/quotes/tag/motivational?page={random_page_num}'

        response = requests.get(URL)
        site = response.text
        soup = BeautifulSoup(site, 'html.parser')

        quotes = soup.find_all(name='div', class_='quoteText')
        quote_list = [quote.get_text().strip().split('\n')[0] for quote in quotes]
        authors = soup.find_all(name='span', class_='authorOrTitle')
        author_list = [author.get_text().strip().title().split(',')[0] for author in authors]

        self.quote = random.choice(quote_list)
        index = quote_list.index(self.quote)
        self.author = author_list[index]

    def get_quote(self):
        return self.quote

    def get_author(self):
        return self.author
