import re
import pandas as pd
from textblob import TextBlob
from collections import Counter
from stop_words import get_stop_words

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from scipy import stats

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


def clean_tweet_hashtags(tweet):
  '''
  Utility function to clean tweet text by removing links, special characters
  using simple regex statements.
  '''
  # Comments to explain this exact regex pattern
  # ((A) | (B) | (C)) - match either A or B or C. Parentheses captures the piece that was matched.
  # A ->  @[A-Za-z0-9]+    Find @ and select the @ plus all letters/numbers after it. (Used to delete usernames)
  # B ->  [^0-9A-Za-z \t]  Select any character that is not a number, letter, space, or tab. (currently deletes #hashtags)
  # C ->  \w+:\/\/\S+      Finds characters, followed by ://, followed by characters. (removes URLs)
  return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t#])|(\w+:\/\/\S+)", " ", tweet).split())

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
      both.append(tweet)
    elif 'coke' in lower_tweet or 'coca cola' in lower_tweet or 'cocacola' in lower_tweet:
      # tweet is only coke
      coke.append(tweet)
    elif 'pepsi' in lower_tweet:
      # tweet is only pepsi
      pepsi.append(tweet)
    else:
      # tweet doesn't fit either category
      leftover.append(tweet)

  return (both, coke, pepsi, leftover)


# Input: list of tweets, should be cleaned beforehand
# Returns: list of sentiment tuples - [(polarity, subjectivity), ...]
#          also prints the number of positive, neutral, and negative results
def get_tweet_sentiments(tweets, positive_list, negative_list):

  sentiments = []

  # keep track of results for debugging purposes
  positive = 0
  neutral = 0
  negative = 0

  print('ANALYZING SENTIMENT')

  for tweet in tqdm(tweets):
    analysis = TextBlob(clean_tweet(tweet))
    sentiments.append(analysis.sentiment)

    # track sentiment results to print
    if analysis.sentiment.polarity > 0:
      positive += 1
      positive_list.append(tweet)
    elif analysis.sentiment.polarity == 0:
      neutral += 1
      negative_list.append(tweet)
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
coke_pos = []
coke_neg = []
coke_sentiments = get_tweet_sentiments(brands[1], coke_pos, coke_neg)

print('pepsi_sentiments')
pepsi_pos = []
pepsi_neg = []
pepsi_sentiments = get_tweet_sentiments(brands[2], pepsi_pos, pepsi_neg)

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


def is_type(word, typelist):
  return word[1] in typelist

noun_t = ["NN", "NNS", "NNP", "NNPS"]
verb_t = ["VB", "VBD"," VBG", "VBN", "VBZ"]
adjective_t = ["JJ", "JJR", "JJS"]

stop_words = get_stop_words('english')
stop_words.append("'s")

def analyze_tweets(tweets):
  giant_list = []
  hashtags = []
  counter = 0
  for tweet in tqdm(tweets):
    analysis = TextBlob(clean_tweet(tweet))
    giant_list += analysis.tags
    hashtags += re.findall(r"#(\w+)", clean_tweet_hashtags(tweet))
    counter += 1

  noun_filtered = list(filter(lambda x: is_type(x, noun_t) and len(x[0]) > 1 and x[0] not in stop_words, giant_list))
  verb_filtered = list(filter(lambda x: is_type(x, verb_t) and len(x[0]) > 1 and x[0] not in stop_words, giant_list))
  adject_filtered = list(filter(lambda x: is_type(x, adjective_t) and len(x[0]) > 1 and x[0] not in stop_words, giant_list))

  nouns = list(map(lambda x: x[0], noun_filtered))
  verbs = list(map(lambda x: x[0], verb_filtered))
  adjectives = list(map(lambda x: x[0], adject_filtered))

  top_nouns = Counter(nouns).most_common(100)
  top_verbs = Counter(verbs).most_common(100)
  top_adjectives = Counter(adjectives).most_common(100)

  top_hashtags = Counter(hashtags).most_common(100)

  return (top_nouns, top_verbs, top_adjectives, top_hashtags)


coke_pos_analysis = analyze_tweets(coke_pos)
coke_neg_analysis = analyze_tweets(coke_neg)
pepsi_pos_analysis = analyze_tweets(pepsi_pos)
pepsi_neg_analysis = analyze_tweets(pepsi_neg)

def print_analysis(analysis):
  print("Top 100 Nouns")
  print(analysis[0])
  print("Top 100 Verbs")
  print(analysis[1])
  print("Top 100 Adjectives")
  print(analysis[2])
  print("Top 100 Hashtags")
  print(analysis[3])

print("########################################\nCoke Positive")
print_analysis(coke_pos_analysis)
print("########################################\nCoke Negative")
print_analysis(coke_neg_analysis)
print("########################################\nPepsi Positive")
print_analysis(pepsi_pos_analysis)
print("########################################\nPepsi Negative")
print_analysis(pepsi_neg_analysis)


# Note: I'm reading that removing objective tweets can improve accuracy of predictions.
#       Not sure what the threshold for that is, so haven't done that yet.

# Note: Choosing not to analyze any tweets that talk about both coke and pepsi.
#       The algorithms probably can't understand both together, which may hurt accuracy.

# Inspired by - http://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/
