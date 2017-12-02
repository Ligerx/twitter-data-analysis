import re
import pandas as pd
from textblob import TextBlob

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from scipy import stats

from tqdm import tqdm


# read & parse data
file1 = "Twitter_Data_One.xlsx"
file2 = "Twitter_Data_Two.xlsx"
df1 = pd.read_excel(file1)
df2 = pd.read_excel(file2)
tweets = df1.append(df2)

# testfile = "Twitter_Data_Test.xlsx"
# df = pd.read_excel(testfile)

# tweets = df["Sound Bite Text"]


def clean_tweet(tweet):
  '''
  Utility function to clean tweet text by removing links, special characters
  using simple regex statements.
  '''
  return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


# Input: All tweets
# Returns: Tuple of 4 lists - (both, coke, pepsi, leftover)
#          which contain cleaned tweet strings belonging to those brands
def segment_brands(tweets):
  both = []
  coke = []
  pepsi = []
  leftover = []

  print('SEGMENTING BRANDS...')

  for tweet in tqdm(tweets):
    cleaned_tweet = clean_tweet(tweet)

    # lower case temp variable for the sake of string comparison
    lower_tweet = cleaned_tweet.lower()

    if ('coke' in lower_tweet or 'coca cola' in lower_tweet or 'cocacola' in lower_tweet) and 'pepsi' in lower_tweet:
      # tweet contains both coke and pepsi text
      both.append(cleaned_tweet)
    elif 'coke' in lower_tweet or 'coca cola' in lower_tweet or 'cocacola' in lower_tweet:
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

  print('ANALYZING SENTIMENT')

  for tweet in tqdm(tweets):
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
  print("total tweets analyzed -", positive + neutral + negative)
  print()

  return sentiments




brands = segment_brands(tweets)

print("--------  Brand Segments  --------")
print("both", len(brands[0]))
print("coke", len(brands[1]))
print("pepsi", len(brands[2]))
print("leftover", len(brands[3]))
print()

print('coke_sentiments')
coke_sentiments = get_tweet_sentiments(brands[1])

print('pepsi_sentiments')
pepsi_sentiments = get_tweet_sentiments(brands[2])



# histogram of sentiment polarity
def extract_polarities(sentiments):
  return list(map(lambda sentiment: sentiment.polarity, sentiments))

def print_stats(brand_name, sentiments):
  print()
  print('Printing stats for', brand_name, '...')

  polarities = extract_polarities(sentiments)
  numpy_array = np.array(polarities)

  print('Mean - ', np.mean(numpy_array))
  print('Median - ', np.median(numpy_array))
  print('Mode - ', stats.mode(numpy_array))

def plot_sentiment_histogram(brand_name, sentiments):
  print()
  print('Printing histogram for', brand_name, '...')

  plt.hist(extract_polarities(sentiments), 60)
  plt.xlabel('Polarity')
  plt.ylabel('Number of Tweets')
  plt.title(brand_name + ' Sentiment Analysis')
  plt.xlim(-1, 1)
  plt.grid(True)
  plt.show()


print_stats('Coke', coke_sentiments)
print_stats('Pepsi', pepsi_sentiments)

plot_sentiment_histogram('Coke', coke_sentiments)
plot_sentiment_histogram('Pepsi', pepsi_sentiments)





# Note: I'm reading that removing objective tweets can improve accuracy of predictions.
#       Not sure what the threshold for that is, so haven't done that yet.

# Note: Choosing not to analyze any tweets that talk about both coke and pepsi.
#       The algorithms probably can't understand both together, which may hurt accuracy.

# Inspired by - http://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/
