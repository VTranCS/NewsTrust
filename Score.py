import Twitter as tw
import math
import time

MONTH_LENGTH = 2.628e6


def scores_from_raw(raw_values):
    to_ret = {}
    # Number of hashtags
    num_hashtags = raw_values['hashtags']
    to_ret['hashtags'] = 5 if num_hashtags < 2 else max(6 - num_hashtags, 0)
    # Number of retweets & likes
    retweets = raw_values['retweets']
    likes = raw_values['likes']

    retweet_score = max(0.0, min(5.0, 1.55 * math.log(retweets / 20)))
    like_score = max(0.0, min(5.0, 1.278 * math.log(retweets / 20)))

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
    return to_ret


def main():
    tw.authenticate()
    user_input = input('What tweet to show? ')
    while user_input != 'exit':
        res = tw.get_id_from_url(user_input)
        tweet = tw.get_tweet_by_id(res)
        raw_values = tw.process_tweet(tweet)
        print(raw_values)
        raw_scores = scores_from_raw(raw_values)
        print(raw_scores)
        user_input = input('What tweet to show? ')


if __name__ == "__main__":
    main()
