import Twitter as tw
import math
import time
import sentimentTest as st
import sentenceAnalysis as sa
import Search

MONTH_LENGTH = 2.628e6


def scores_from_raw(raw_values):
    to_ret = {}
    # Number of hashtags
    num_hashtags = raw_values['hashtags']
    to_ret['hashtags'] = 5 if num_hashtags < 2 else max(6 - num_hashtags, 0)
    # Number of retweets & likes
    retweets = raw_values['retweets']
    likes = raw_values['likes']

    retweet_score = max(0.0, min(5.0, 1.55 * math.log((1 + retweets) / 20)))
    like_score = max(0.0, min(5.0, 1.278 * math.log((1 + likes) / 20)))

    to_ret['retweets'] = retweet_score
    to_ret['likes'] = like_score

    # Verified on Twitter
    verified = raw_values['verified']
    to_ret['verified'] = 5 if verified else 0
    # Length of tweet (weight low)
    length = raw_values['length']
    to_ret['length'] = min(5 * length / 140, 5)
    # Date
    time_written = raw_values['written']
    time_now = int(time.time())
    diff = time_now - time_written
    old_tweet = diff > MONTH_LENGTH
    to_ret['written'] = MONTH_LENGTH / diff * 5 if old_tweet else 5
    # Date of account creation
    time_created = raw_values['created']
    diff = time_now - time_created
    old_account = diff > MONTH_LENGTH
    to_ret['created'] = 5 if old_account else diff / MONTH_LENGTH * 5

    # Sentiment analysis
    text = raw_values['text']
    direction, mag = st.sentimentDetection(text)
    to_ret['direction'] = direction
    to_ret['magnitude'] = mag

    # Sentence Analysis
    to_ret['cap'] = sa.capitalization(text)
    to_ret['compx'] = sa.sentenceComplexity(text)
    to_ret['misspell'] = sa.mispells(text)
    return to_ret


def aggregate(raw_scores):
    complexity = 7.44 * raw_scores['compx']
    capitalization = 6.46 * raw_scores['cap']
    spelling = 6.46 * raw_scores['misspell']
    hashtags = 7.96 * raw_scores['hashtags']
    retweets = 2.97 * raw_scores['retweets']
    likes = 2.97 * raw_scores['likes']
    verified = 13.93 * raw_scores['verified']
    length = 4.97 * raw_scores['length']
    written = 7.96 * raw_scores['written']
    created = 10.94 * raw_scores['created']
    magnitude = 27.94 * raw_scores['magnitude']
    scores = [complexity, capitalization, spelling, hashtags, retweets, likes, verified, length, written, created, magnitude]
    return max(0, (sum(scores) / 100 - 3) * 5 / 2)


def process_tweet_url(url):
    res = tw.get_id_from_url(url)
    tweet = tw.get_tweet_by_id(res)
    raw_values = tw.process_tweet(tweet)
    raw_scores = scores_from_raw(raw_values)
    aggregate_score = aggregate(raw_scores)
    pf_url = Search.build_politifact_url_from_tweet(tweet)
    pf = Search.scrape_politifact(pf_url)
    if tweet['user']['verified']:
        gl_url = Search.build_google_url_from_tweet(tweet)
        wiki_lnk = Search.scrape_author(gl_url)
        wiki_title = 'Wikipedia'
        wiki = (wiki_lnk, wiki_title)
    else:
        wiki = ('Could Not Find A Link', '')
    return {'score': aggregate_score, 'wiki': wiki, 'politifact': pf}


def main():
    tw.authenticate()
    user_input = input('What tweet to show? ')
    while user_input != 'exit':
        res = process_tweet_url(user_input)
        print(res)
        user_input = input('What tweet to show? ')


if __name__ == "__main__":
    main()
