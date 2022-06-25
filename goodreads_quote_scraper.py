import argparse
import re
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import csv
import os
ap = argparse.ArgumentParser(description='Scrape quotes from Goodreads.com')

ap.add_argument("-t", "--tag",
                required=False, type=str, default=None,
                help="tag (topic/theme) of quotes to scrape")
ap.add_argument("-p", "--max_pages",
                required=False, type=int, default=10,
                help="maximum number of webpages to scrape")
ap.add_argument("-q", "--max_quotes",
                required=False, type=int, default=100,
                help="maximum number of quotes to scrape")

args = vars(ap.parse_args())
def download_goodreads_quotes(tag, max_pages=1, max_quotes=50):

    def download_quotes_from_page(tag, page):

        def compile_url(tag, page):
            return f'https://www.goodreads.com/quotes/tag/{tag}?page={page}'

        def get_soup(url):
            response = urlopen(Request(url))
            return BeautifulSoup(response, 'html.parser')

        def extract_quotes_elements_from_soup(soup):
            elements_quotes = soup.find_all("div", {"class": "quote mediumText"})
            return elements_quotes

        def extract_quote_dict(quote_element):

            def extract_quote(quote_element):
                try:
                    quote = quote_element.find('div', {'class': 'quoteText'}).get_text("|", strip=True)
                    # first element is always the quote
                    quote = quote.split('|')[0]
                    quote = re.sub('^“', '', quote)
                    quote = re.sub('”\s?$', '', quote)
                    return quote
                except:
                    return None

            def extract_author(quote_element):
                try:
                    author = quote_element.find('span', {'class': 'authorOrTitle'}).get_text()
                    author = author.strip()
                    author = author.rstrip(',')
                    return author
                except:
                    return None

            def extract_source(quote_element):
                try:
                    source = quote_element.find('a', {'class': 'authorOrTitle'}).get_text()
                    return source
                except:
                    return None

            def extract_tags(quote_element):
                try:
                    tags = quote_element.find('div', {'class': 'greyText smallText left'}).get_text(strip=True)
                    tags = re.sub('^tags:', '', tags)
                    tags = tags.split(',')
                    return tags
                except:
                    return None

            def extract_likes(quote_element):
                try:
                    likes = quote_element.find('a', {'class': 'smallText', 'title': 'View this quote'}).get_text(strip=True)
                    likes = re.sub('likes$', '', likes)
                    likes = likes.strip()
                    return int(likes)
                except:
                    return None

            quote_data = {'quote': extract_quote(quote_element),
                          'author': extract_author(quote_element),
                          'source': extract_source(quote_element),
                          'likes': extract_likes(quote_element),
                          'tags': extract_tags(quote_element)}

            return quote_data

        url = compile_url(tag, page)
        print(f'Retrieving {url}...')
        soup = get_soup(url)
        quote_elements = extract_quotes_elements_from_soup(soup)

        return [extract_quote_dict(e) for e in quote_elements]

  #   def download_all_pages(tag, max_pages, max_quotes,min_pages):
# def download_all_pages(tag, max_pages, max_quotes,min_pages):
    def download_all_pages(tag, max_pages, max_quotes):
        results = []
        p = 4
        while p <= max_pages:
            res = download_quotes_from_page(tag, p)
            if len(res) == 0:
                print(f'No results found on page {p}.\nTerminating search.')
                return results

            results = results + res

            if len(results) >= max_quotes:
                print(f'Hit quote maximum ({max_quotes}) on page {p}.\nDiscontinuing search.')
                return results[0:max_quotes]
            else:
                p += 1

        return results
    return download_all_pages(tag, max_pages, max_quotes)
   # return download_all_pages(tag, max_pages, max_quotes,min_pages)
def recreate_quote(dict):
    return f'"{dict.get("quote")}" - {dict.get("author")}'

def save_quotes(quote_data, tag):
    save_path = os.path.join(os.getcwd(), 'scraped' + '-' + tag + '.txt')
    print('saving file')
    with open(save_path, 'w', encoding='utf-8') as f:
        quotes = [recreate_quote(q) for q in quote_data]
        for q in quotes:
            f.write(q + '\n')
if __name__ == '__main__':
    tag = args['tag'] if args['tag'] != None else input('Provide tag to search quotes for: ')
    mp = args['max_pages']
    mq = args['max_quotes']
    result = download_goodreads_quotes(tag, max_pages=mp, max_quotes=mq)
    save_quotes(result, tag)
"""
goodreads-scraper.py -t 'bias' -p 3 -q
"""
