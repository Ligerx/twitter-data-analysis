import re
import pandas as pd
from textblob import TextBlob
from collections import Counter
from stop_words import get_stop_words

# read & parse data
file1 = "Twitter_Data_One.xlsx"
file2 = "Twitter_Data_Two.xlsx"
df1 = pd.read_excel(file1)
df2 = pd.read_excel(file2)

tweets1 = df1["Sound Bite Text"]
tweets2 = df2["Sound Bite Text"]
tweets = pd.concat([tweets1, tweets2])
print("DONE: reading")

# testing with a smaller file
# testfile = "Twitter_Data_Test.xlsx"
# df = pd.read_excel(testfile)
# tweets = df["Sound Bite Text"]

def segment_brands(tweets):
  both = []
  coke = []
  pepsi = []
  leftover = []

  for tweet in tweets:
    # lower case temp variable for the sake of string comparison
    lower_tweet = tweet.lower()

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


both, coke, pepsi, leftover = segment_brands(tweets)

def is_type(word, typelist):
	return word[1] in typelist

noun_t = ["NN", "NNS", "NNP", "NNPS"]
verb_t = ["VB", "VBD"," VBG", "VBN", "VBZ"]
adjective_t = ["JJ", "JJR", "JJS"]

stop_words = get_stop_words('english')

def analyze_tweets(tweets):
	giant_list = []
	hashtags = []
	counter = 0
	for tweet in tweets:
		analysis = TextBlob(tweet)
		giant_list += analysis.tags
		hashtags += re.findall(r"#(\w+)", tweet)
		print(counter)
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

print("coke analysis")
coke_analysis = analyze_tweets(coke)
print("pepsi analysis")
pepsi_analysis = analyze_tweets(pepsi)
