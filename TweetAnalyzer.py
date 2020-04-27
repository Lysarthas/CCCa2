import fileinput
import json
import re

# install nltk through anaconda or binary distribution pip install nltk
import nltk
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
#from collections import defaultdict
#from nltk.corpus import wordnet

# use the lemmatizer to find the lemma for each tweet token
lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()
nltk.download('words')
nltk.download('averaged_perceptron_tagger')
words = set(nltk.corpus.words.words())

tt = TweetTokenizer()
nltk.download('stopwords')
stopwords = set(stopwords.words('english'))


def process_twitter_json(file_name):
    rows = []
    bow = {}

    file = open(str(file_name), 'r', encoding='utf8')
    while True:
        line = file.readline()
        if not line:
            break
        rows.append(line)
    file.close()

    tweets = []
    hashTagDict = {}
    print(len(rows))

    for row in rows:
        if not row:
            break
        tweetLine = json.loads(row)

        lang = tweetLine['lang']
        tweetText = tweetLine['text']
        tweets.append(tweetText)
        tokens = tt.tokenize(tweetText)
        # calculate the bag of word representation for each tweet
        for token in tokens:
            # do not add to bag-of-words if it is a stop-word
            lemma = lemmatizer.lemmatize(token.lower())
            if lemma not in stopwords:        #and lemma in words
                bow[lemma] = bow.get(lemma, 0) + 1

    for tweet in tweets:
        tags = re.findall(r"(#\w+)", tweet)
        for tag in tags:
            tag = tag.lower()
            if tag in hashTagDict:
                hashTagDict[tag] +=1
            else:
                hashTagDict[tag] = 1

    sortedBOW = {langKey: count for langKey, count in sorted(bow.items(), key=lambda item: item[1], reverse=True)[:1000]}
    sortedTagDict = {tagKey: count for tagKey, count in sorted(hashTagDict.items(), key=lambda item: item[1], reverse=True)[:20]}

    print('Top tags')
    print(sortedTagDict)

    print('Top Bag of Words')
    print(sortedBOW)


# replace this with the crawled tweets.json file
process_twitter_json("tweets.json")



