from json import loads as jsread

from wordcloud import WordCloud
from wordcloud_fa import WordCloudFa
import numpy as np
from PIL import Image

import os

import arabic_reshaper

def fetch_tweet(idish):
	f = open("out/tweets.json","w")
	f.write("")
	f.close()

	os.popen(f"twint -u {idish} -o out/tweets.json --stats --json --filter-retweets --limit 16384").read()


def ok(t):
	#if len(t['mentions'])>0 : return False
	if len(t['retweet_date'])>0 : return False
	if len(t['quote_url'])>0 : return False
	if len(t['photos'])>0 : return False


	return True

def clean(d):
    d.replace("\u200c","")
    if "t.co" in d : return ""
    if len(d) <3: return ""

    if " می" in d  or "شه" in d  : return ""
    if "بیش" in d  : return ""
    if "می" in d : return ""
    if d == "ست" : return ""
    if "خیلی" in d : return ""
    if "ولی" in d : return ""


    return d

def get_stopwords():
	with open("assets/stop_words/additional_stops.txt") as f:
		words = [i.strip() for i in f.readlines()]
	with open("assets/stop_words/stopwords_me.txt") as f:
		words += [i.strip() for i in f.readlines()]
	return words


def make(idish, mask = "twitter"):
	fetch_tweet(idish)

	tweet_file = open("out/tweets.json","r").read()
	tweet_json_str = tweet_file.split("\n")

	tweet_dict = []
	for i in range(len(tweet_json_str)-1):
		t = tweet_json_str[i]
		d = jsread(t)

		if not ok(d): continue
		tweet_dict.append(d)


	tweets_simple = [ clean(t['tweet']) for t in tweet_dict ]

	to_print = "\n\n".join(tweets_simple)

	f = open("out/cleaned.txt","w")
	f.write(to_print)
	f.close()

	mask_array = np.array(
		Image.open(f"assets/masks/{mask}.png")
	)

	with open('out/cleaned.txt', 'r') as file:
		text = file.read()

		wc = WordCloudFa(
			width=900, height=900,
			background_color="white",
			mask = mask_array,
			include_numbers=False,
			persian_normalize=True,
		)
		
		wc.add_stop_words(get_stopwords())

		word_cloud = wc.generate(text)

		image = word_cloud.to_image()
		image.save(f"out/{idish}.png")
