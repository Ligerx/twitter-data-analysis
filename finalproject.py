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




# def get_tweet_sentiment(tweet):
#     '''
#     Utility function to classify sentiment of passed tweet
#     using textblob's sentiment method
#     '''

#     # tweet


#     # create TextBlob object of passed tweet text
#     analysis = TextBlob(clean_tweet(tweet))
#     # set sentiment
#     if analysis.sentiment.polarity > 0:
#         return 'positive'
#     elif analysis.sentiment.polarity == 0:
#         return 'neutral'
#     else:
#         return 'negative'


# negative = 0
# positive = 0
# neutral = 0
# for tweet in tweets:
# 	sent = get_tweet_sentiment(clean_tweet(tweet))
# 	if sent == 'positive':
# 		positive += 1
# 	elif sent == 'negative':
# 		negative += 1
# 	else:
# 		neutral += 1



# Input: All tweets
# Returns: Tuple of 4 lists - (both, coke, pepsi, leftover)
#          which contain cleaned tweet strings belonging to those brands
def segment_brands(tweets):
  both = []
  coke = []
  pepsi = []
  leftover = []

  for tweet in tweets:
    cleaned_tweet = clean_tweet(tweet)

    # lower case temp variable for the sake of string comparison
    lower_tweet = cleaned_tweet.lower()

    if ('coke' in lower_tweet or 'coca cola' in lower_tweet) and 'pepsi' in lower_tweet:
      # tweet contains both coke and pepsi text
      both.append(cleaned_tweet)
    elif 'coke' in lower_tweet or 'coca cola' in lower_tweet:
      # tweet is only coke
      coke.append(cleaned_tweet)
    elif 'pepsi' in lower_tweet:
      # tweet is only pepsi
      pepsi.append(cleaned_tweet)
    else:
      # tweet doesn't fit either category
      leftover.append(cleaned_tweet)

  return (both, coke, pepsi, leftover)


# Input: list of tweets, should be cleaned beforehand
# Returns: list of sentiment tuples - [(polarity, subjectivity), ...]
#          also prints the number of positive, neutral, and negative results
def get_tweet_sentiments(tweets):
  sentiments = []

  # keep track of results for debugging purposes
  positive = 0
  neutral = 0
  negative = 0

  for tweet in tweets:
    analysis = TextBlob(tweet)
    sentiments.append(analysis.sentiment)

    # track sentiment results to print
    if analysis.sentiment.polarity > 0:
      positive += 1
    elif analysis.sentiment.polarity == 0:
      neutral += 1
    else:
      negative += 1

  print("--------  get_tweet_sentiments  --------")
  print("positive - ", positive)
  print("neutral - ", neutral)
  print("negative - ", negative)
  print()

  return sentiments


brands = segment_brands(tweets)
