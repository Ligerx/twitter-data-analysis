import re
import pandas as pd
from textblob import TextBlob

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import norm

from tqdm import tqdm, tqdm_pandas


# read & parse data
file1 = "Twitter_Data_One.xlsx"
file2 = "Twitter_Data_Two.xlsx"
print('READING IN THE DATA...')
df1 = pd.read_excel(file1)
df2 = pd.read_excel(file2)
tweets1 = df1["Sound Bite Text"]
tweets2 = df2["Sound Bite Text"]
tweets = pd.concat([tweets1, tweets2])

# testing with a smaller file
# testfile = "Twitter_Data_Test.xlsx"
# df = pd.read_excel(testfile)
# tweets = df["Sound Bite Text"]

print('DONE READING DATA...')
print('# of rows - ', len(tweets))


def clean_tweet(tweet):
  '''
  Utility function to clean tweet text by removing links, special characters
  using simple regex statements.
  '''
  # Comments to explain this exact regex pattern
  # ((A) | (B) | (C)) - match either A or B or C. Parentheses captures the piece that was matched.
  # A ->  @[A-Za-z0-9]+    Find @ and select the @ plus all letters/numbers after it. (Used to delete usernames)
  # B ->  [^0-9A-Za-z \t]  Select any character that is not a number, letter, space, or tab. (currently deletes #hashtags)
  # C ->  \w+:\/\/\S+      Finds characters, followed by ://, followed by characters. (removes URLs)
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

def plot_sentiment_histogram(brand_name, sentiments, remove_zeros=False):
  print()
  print('Printing histogram for', brand_name, '...')

  polarities = extract_polarities(sentiments)

  if remove_zeros:
    polarities = list(filter(lambda x: x != 0, polarities))

  # best fit of data
  mu, std = norm.fit(polarities)

  # Draw the histogram
  # n, bins, patches = plt.hist(polarities, bins=60)
  plt.hist(polarities, bins=60)

  # # Draw a best fit line
  # y = mlab.normpdf(bins, mu, sigma)
  # plt.plot(bins, y, 'r--', linewidth = 2)

  # set the x range
  xmin, xmax = -1, 1
  plt.xlim(xmin, xmax)

  # Draw best fit line
  x = np.linspace(xmin, xmax)
  p = norm.pdf(x, mu, std)
  plt.plot(x, p, 'k', linewidth=2)


  plt.xlabel('Polarity')
  plt.ylabel('Number of Tweets')
  plt.title(brand_name + ' Sentiment Analysis')
  plt.grid(True)
  plt.show()


print_stats('Coke', coke_sentiments)
print_stats('Pepsi', pepsi_sentiments)

plot_sentiment_histogram('Coke', coke_sentiments)
plot_sentiment_histogram('Pepsi', pepsi_sentiments)


plot_sentiment_histogram('Coke (w/o 0s)', coke_sentiments, True)
plot_sentiment_histogram('Pepsi (w/o 0s)', pepsi_sentiments, True)


# Note: I'm reading that removing objective tweets can improve accuracy of predictions.
#       Not sure what the threshold for that is, so haven't done that yet.

# Note: Choosing not to analyze any tweets that talk about both coke and pepsi.
#       The algorithms probably can't understand both together, which may hurt accuracy.

# Inspired by - http://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/
