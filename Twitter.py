import base64
import requests
import urllib.parse
import datetime
import calendar
import pprint
import os

TOKEN = None

base_url = 'https://api.twitter.com/'
auth_url = '{}oauth2/token'.format(base_url)
show_url = '{}1.1/statuses/show.json'.format(base_url)


def get_bearer_token(consumer_key=os.environ['CONSUMER_KEY'], consumer_secret=os.environ['CONSUMER_SECRET']):
    consumer_key = urllib.parse.quote(consumer_key)
    consumer_secret = urllib.parse.quote(consumer_secret)
    bearer_token = consumer_key + ':' + consumer_secret
    base64_encoded_bearer_token = base64.b64encode(bearer_token.encode('utf-8'))

    headers = {
        "Authorization": "Basic " + base64_encoded_bearer_token.decode('utf-8') + "",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Content-Length": "29"}

    response = requests.post(auth_url, headers=headers, data={'grant_type': 'client_credentials'})
    to_json = response.json()
    return to_json['access_token'] if response.status_code == 200 else None


def authenticate():
    global TOKEN
    TOKEN = get_bearer_token()


def get_id_from_url(url):
    return url.strip().split('/')[-1]


def get_tweet_by_id(id, access_token=None):
    if access_token is None:
        access_token = TOKEN
    header = {
        'Authorization': 'Bearer {}'.format(access_token),
    }
    show_params = {
        'id': id,
        'tweet_mode': 'extended',
    }

    search_resp = requests.get(show_url, headers=header, params=show_params)
    # pprint.pprint(search_resp.json())
    return search_resp.json()


def process_tweet(tweet):
    to_ret = {}
    # Number of hashtags
    to_ret['hashtags'] = len(tweet['entities']['hashtags'])
    # Number of retweets & likes
    to_ret['likes'] = int(tweet['favorite_count'])
    to_ret['retweets'] = int(tweet['retweet_count'])
    # Verified on Twitter
    to_ret['verified'] = bool(tweet['user']['verified'])
    # Length of tweet (weight low)
    to_ret['length'] = len(tweet['full_text'])
    # Date
    date_format = '%a %b %d %H:%M:%S %z %Y'
    written_date = tweet['created_at']
    written = datetime.datetime.strptime(written_date, date_format)
    to_ret['written'] = calendar.timegm(written.timetuple())
    # Date of account creation
    created_date = tweet['user']['created_at']
    created = datetime.datetime.strptime(created_date, date_format)
    to_ret['created'] = calendar.timegm(created.timetuple())
    return to_ret


def main():
    authenticate()
    user_input = input('What tweet to show? ')
    while user_input != 'exit':
        res = get_id_from_url(user_input)
        tweet = get_tweet_by_id(res)
        print(process_tweet(tweet))
        user_input = input('What tweet to show? ')


if __name__ == "__main__":
    main()
