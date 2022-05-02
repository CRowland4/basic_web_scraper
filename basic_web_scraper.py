import sys

from bs4 import BeautifulSoup
import requests
import string
import os


def _format_article_title(article_title):
    """Formats the title of the given article."""
    formatted_title = article_title

    for character in formatted_title[:]:
        if character in string.punctuation:
            formatted_title = formatted_title.replace(character, '')

    formatted_title = formatted_title.replace(' ', '_')
    return formatted_title


class Scraper:
    def __init__(self):
        self.response = None
        self.soup = None
        self.requested_pages = 0
        self.current_page_number = 1
        self.article_type = ''

    def main(self):
        self._set_user_request()

        while self.current_page_number <= self.requested_pages:
            self._set_response()
            self._validate_response()
            self._set_soup()
            self._create_directory()
            self._get_content()
            self.current_page_number += 1

        return

    def _set_user_request(self):
        """Gets the number of pages to scrape and the article type from the user."""
        self.requested_pages = int(input("How many pages would you like to search?:\n"))
        self.article_type = input("\nWhat type of article are you looking for?:\n")
        return

    def _set_response(self):
        """Sets the response object for the current page number."""
        page = self.current_page_number
        url = f'https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&year=2020&page={page}'
        self.response = requests.get(url)
        return

    def _validate_response(self):
        """Confirms that the request was successful."""
        if self.response.status_code == 200:
            return

        print(f'Error {self.response.status_code}.')
        sys.exit()

    def _set_soup(self):
        """Sets the soup attribute."""
        self.soup = BeautifulSoup(self.response.content, 'html.parser')
        return

    def _create_directory(self):
        """Creates a directory to store articles from the current page number."""
        os.mkdir(f'Page_{self.current_page_number}')
        return

    def _get_content(self):
        """Saves the articles' content from the current page into their own file."""
        articles = self.soup.find_all('article')

        for article in articles:
            type_tag = article.find('span', class_='c-meta__item c-meta__item--block-at-lg')
            if type_tag.text.strip() == f'{self.article_type}':
                link_tag = article.find('a', attrs={'data-track-action': "view article"})
                article_title = link_tag.get_text()
                formatted_title = _format_article_title(article_title)
                url = 'https://www.nature.com' + str(link_tag['href'])
                article_response = requests.get(url)
                article_soup = BeautifulSoup(article_response.content, 'html.parser')
                article_body = article_soup.find('div', class_='c-article-body u-clearfix').get_text()

                with open(f'Page_{self.current_page_number}\\{formatted_title}.txt', 'w', encoding='utf-8') as file:
                    file.write(article_body)  # TODO this gets the content, need to come back and clean it up a bit.

        return


my_scraper = Scraper()
my_scraper.main()


