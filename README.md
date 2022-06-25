# Goodread quote scaper
How to use: type in the command line for windows
 goodreads_quote_scraper.py -t 'bias' -p 3 -q
"-t", "--tag", required=False, type=str, default=None, help="tag (topic/theme) of quotes to scrape"
"-p", "--max_pages", required=False, type=int, default=10, help="maximum number of webpages to scrape"
"-q", "--max_quotes", required=False, type=int, default=100, help="maximum number of quotes to scrape"
