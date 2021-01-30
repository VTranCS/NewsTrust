import urllib.parse
import requests
from bs4 import BeautifulSoup
import Twitter as tw

politifact_base_url = 'https://www.politifact.com/search/?q='


def build_url_from_tweet(tweet):
    body = tweet['full_text']
    query = urllib.parse.quote_plus(body)
    return politifact_base_url + query


def scrape_page(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    source = soup.find_all(class_="c-textgroup__title")[0].find('a')
    title = source.get_text().strip()
    lnk = 'https://www.politifact.com' + source['href']
    print(title)
    print(lnk)


def main():
    tw.authenticate()
    user_input = input('What tweet to show? ')
    while user_input != 'exit':
        res = tw.get_id_from_url(user_input)
        tweet = tw.get_tweet_by_id(res)
        print(tw.process_tweet(tweet))
        url = build_url_from_tweet(tweet)
        scrape_page(url)
        user_input = input('What tweet to show? ')


if __name__ == "__main__":
    main()
