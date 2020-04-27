import tweepy

consumer_key = 'h1dqkm4wP9vui7U3snEMS0Z6A'
consumer_secret = 'm20fMBT1Ijx7yNS9PXf8hSmYix8TgkkNtp3YHin0EO7UWiROFZ'
access_token = '1170264592410267648-SZUOk09ew5EAURbUcPvEi4PoyCGMB0'
access_secret = 'EsgTim4FkLeYxmjX1baOUKbeGgj2YDwf2BknHkxLr1Tfu'

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