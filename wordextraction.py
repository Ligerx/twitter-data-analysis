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

nouns = ["NN", "NNS", "NNP", "NNPS"]
verbs = ["VB", "VBD"," VBG", "VBN", "VBZ"]
adjectives = ["JJ", "JJR", "JJS"]

noun_words = list(filter(lambda x: is_type(x, nouns), giant_list))
verb_words = list(filter(lambda x: is_type(x, verbs), giant_list))
adject_words = list(filter(lambda x: is_type(x, adjectives), giant_list))

