import re
import pandas as pd
from textblob import TextBlob


# read & parse data
# file1 = "Twitter_Data_One.xlsx"
# file2 = "Twitter_Data_Two.xlsx"
# df1 = pd.read_excel(file1)
# df2 = pd.read_excel(file2)

testfile = "Twitter_Data_Test.xlsx"
df = pd.read_excel(testfile)

tweets = df["Sound Bite Text"]



# sentiment analysis
# http://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/
def clean_tweet(tweet):
    '''
    Utility function to clean tweet text by removing links, special characters
    using simple regex statements.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def get_tweet_sentiment(tweet):
    '''
    Utility function to classify sentiment of passed tweet
    using textblob's sentiment method
    '''
    # create TextBlob object of passed tweet text
    analysis = TextBlob(clean_tweet(tweet))
    # set sentiment
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'


negative = 0
positive = 0
neutral = 0
for tweet in tweets:
	sent = get_tweet_sentiment(clean_tweet(tweet))
	if sent == 'positive':
		positive += 1
	elif sent == 'negative':
		negative += 1
	else:
		neutral += 1


# make it look nice