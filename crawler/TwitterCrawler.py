import tweepy

consumer_key = 'cGrAaG5mkE6t4wnBbcUJ3PlrY'
consumer_secret = 'm95G2ZzDoW45aQaK1KajBjYZBETtcWeJBkWNcuCoUgPJMbrWe4'
access_token = '1170264592410267648-eeYlYJuUBfcd1B0fsm0EibgrCYnSMM'
access_secret = 'tPq5g4FWN4xNxTyPANWdprpU4jeKBrmist2kniM5jXdmn'

tweetsPerQry = 100
maxTweets = 1000000
hashtag = "#covid"

authentication = tweepy.OAuthHandler(consumer_key, consumer_secret)
authentication.set_access_token(access_token, access_secret)
api = tweepy.API(authentication, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
maxId = -1
tweetCount = 0
while tweetCount < maxTweets:
    if (maxId <= 0):
        newTweets = api.search(q=hashtag, count=tweetsPerQry, result_type="recent", tweet_mode="extended")
    else:
        newTweets = api.search(q=hashtag, count=tweetsPerQry, max_id=str(maxId - 1), result_type="recent",
                               tweet_mode="extended")

    if not newTweets:
        break

    for tweet in newTweets:
        print(tweet.full_text.encode('utf-8'))

    tweetCount += len(newTweets)
    maxId = newTweets[-1].id