import re
import pandas as pd
from textblob import TextBlob
from collections import Counter

# read & parse data
# file1 = "Twitter_Data_One.xlsx"
# file2 = "Twitter_Data_Two.xlsx"
# df1 = pd.read_excel(file1)
# df2 = pd.read_excel(file2)

testfile = "Twitter_Data_Test.xlsx"
df = pd.read_excel(testfile)

tweets = df["Sound Bite Text"]

# http://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/
def clean_tweet(tweet):
    '''
    Utility function to clean tweet text by removing links, special characters
    using simple regex statements.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

giant_list = []


# TODO: hashtags
for tweet in tweets:
	analysis = TextBlob(clean_tweet(tweet))
	giant_list += analysis.tags

def is_type(word, typelist):
	return word[1] in typelist

noun_t = ["NN", "NNS", "NNP", "NNPS"]
verb_t = ["VB", "VBD"," VBG", "VBN", "VBZ"]
adjective_t = ["JJ", "JJR", "JJS"]

noun_filtered = list(filter(lambda x: is_type(x, noun_t), giant_list))
verb_filtered = list(filter(lambda x: is_type(x, verb_t), giant_list))
adject_filtered = list(filter(lambda x: is_type(x, adjective_t), giant_list))

nouns = list(map(lambda x: x[0], noun_filtered))
verbs = list(map(lambda x: x[0], verb_filtered))
adjectives = list(map(lambda x: x[0], adject_filtered))

top_nouns = Counter(nouns).most_common(100)  
top_verbs = Counter(verbs).most_common(100)
top_adjectives = Counter(adjectives).most_common(100)

