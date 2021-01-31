import urllib.parse
import requests
import re
from bs4 import BeautifulSoup
import Twitter as tw

politifact_base_url = 'https://www.politifact.com/search/?q='
google_base_url = 'https://www.google.com/search?q='


def build_politifact_url_from_tweet(tweet):
    body = tweet['full_text']
    query = urllib.parse.quote_plus(body)
    return politifact_base_url + query


def build_google_url_from_tweet(tweet):
    query = urllib.parse.quote_plus(tweet['user']['name'])
    return google_base_url + query


def scrape_politifact(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    source = soup.find_all(class_="c-textgroup__title")[0].find('a')
    title = source.get_text().strip()
    lnk = 'https://www.politifact.com' + source['href']
    # print(title)
    # print(lnk)
    return title, lnk


def scrape_author(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    wiki = soup.find('a', href=re.compile('/url\?q=https://en.wikipedia.org/'))
    lnk = wiki['href'].split('&')[0][7:]
    # print(lnk)
    return lnk


def main():
    tw.authenticate()
    user_input = input('What tweet to show? ')
    while user_input != 'exit':
        res = tw.get_id_from_url(user_input)
        tweet = tw.get_tweet_by_id(res)
        print(tw.process_tweet(tweet))
        pf_url = build_politifact_url_from_tweet(tweet)
        scrape_politifact(pf_url)
        auth_url = build_google_url_from_tweet(tweet)
        scrape_author(auth_url)
        user_input = input('What tweet to show? ')


if __name__ == "__main__":
    main()
