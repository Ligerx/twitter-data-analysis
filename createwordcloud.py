import re
from os import path
from PIL import Image
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import wordcloud
from stop_words import get_stop_words
from random import randint

def show(wc):
	plt.figure(figsize=(15,8))
	plt.imshow(wc)
	plt.axis("off")
	plt.show()

def segment_brands(tweets):
	both = ""
	coke = ""
	pepsi = ""
	leftover = ""

	for tweet in tweets:
		# lower case temp variable for the sake of string comparison
		lower_tweet = tweet.lower()

		if ('coke' in lower_tweet or 'coca cola' in lower_tweet or 'cocacola' in lower_tweet) and 'pepsi' in lower_tweet:
			# tweet contains both coke and pepsi text
			both += tweet
		elif 'coke' in lower_tweet or 'coca cola' in lower_tweet or 'cocacola' in lower_tweet:
			# tweet is only coke
			coke += tweet
		elif 'pepsi' in lower_tweet:
			# tweet is only pepsi
			pepsi += tweet
		else:
			# tweet doesn't fit either category
			leftover += tweet

	return (both, coke, pepsi, leftover)

def coke_color(word, font_size, position, orientation, random_state=None, **kwargs):
	colors = ["red", "white"]
	return colors[0]

def pepsi_color(word, font_size, position, orientation, random_state=None, **kwargs):
	colors = ["red", "blue", "white"]
	return colors[randint(0,2)]


# read & parse data
file1 = "Twitter_Data_One.xlsx"
file2 = "Twitter_Data_Two.xlsx"
df1 = pd.read_excel(file1)
df2 = pd.read_excel(file2)

tweets1 = df1["Sound Bite Text"]
tweets2 = df2["Sound Bite Text"]
tweets = pd.concat([tweets1, tweets2])
print("DONE: reading")

# # testing with a smaller file
# testfile = "Twitter_Data_Test.xlsx"
# df = pd.read_excel(testfile)
# tweets = df["Sound Bite Text"]

both, coketext, pepsitext, leftover = segment_brands(tweets)


stopwords = get_stop_words('english')
stopwords.append("'s")
coke_stopwords = set(['Coke', 'Coca-Cola', 'Coca', 'coke', 'Cola', 'cocacola', 'cola', 'twitter', 'Twitter', 'com', 'RT'])
coke_stopwords = coke_stopwords.union(stopwords)

coke_wc = wordcloud.WordCloud(background_color = 'white', width = 1000, height = 500, stopwords = coke_stopwords).generate(coketext)
coke_wc.recolor(color_func = coke_color)
show(coke_wc)

stopwords = get_stop_words('english')
stopwords.append("'s")
pepsi_stopwords = set(['Pepsi', 'pepsi', 'cola', 'twitter', 'Twitter', 'com', 'RT'])
pepsi_stopwords = pepsi_stopwords.union(stopwords)

pepsi_wc = wordcloud.WordCloud(background_color = 'black', width = 1000, height = 500, stopwords = pepsi_stopwords).generate(pepsitext)
pepsi_wc.recolor(color_func = pepsi_color)
show(pepsi_wc)

