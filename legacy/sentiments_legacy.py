from flask import Blueprint, render_template, request
import matplotlib.pyplot as plt
import os
import tweepy
import csv
import re
from textblob import TextBlob

import matplotlib
matplotlib.use('agg')

# Register this file as a blueprint
second = Blueprint("second", __name__, static_folder="static", template_folder="template")

# Render page when URL is called
@second.route("/sentiment_analyzer")
def sentiment_analyzer():
    return render_template("sentiment_analyzer.html")

# Class with main logic
class SentimentAnalysis:

    def __init__(self):
        self.tweets = []
        self.tweetText = []

    # This function connects to the Tweepy API and downloads tweet data
    def DownloadData(self, keyword, tweets,bear):
        # Authenticating with Bearer Token (API v2)
        bearer_token = bear # Reemplaza con tu Bearer Token real
        client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)

        # Convert tweets to integer
        tweets = int(tweets)

        # Searching for tweets with API v2
        # Nota: La API v2 tiene límites diferentes en la cantidad de tweets que puedes obtener
        self.tweets = client.search_recent_tweets(
            query=keyword,
            max_results=tweets if tweets <= 100 else 100,  # Máximo 100 tweets en el plan básico
            tweet_fields=['created_at', 'text'],
            user_fields=['profile_image_url'],
            expansions=['author_id']
        )

        # Open/create a file to append data to
        csvFile = open('result.csv', 'a')
        csvWriter = csv.writer(csvFile)

        # Creating variables to store sentiment info
        polarity = 0
        positive = 0
        spositive = 0
        negative = 0
        snegative = 0
        neutral = 0

        # Iterating through tweets fetched
        if self.tweets.data:
            for tweet in self.tweets.data:
                # Append cleaned tweet text to list
                self.tweetText.append(self.cleanTweet(tweet.text).encode('utf-8'))
                analysis = TextBlob(tweet.text)
                polarity += analysis.sentiment.polarity

                # Categorize sentiment (same logic as before)
                if -0.2 < analysis.sentiment.polarity <= 0.2:
                    neutral += 1
                elif 0.2 < analysis.sentiment.polarity <= 0.5:
                    positive += 1
                elif 0.5 < analysis.sentiment.polarity <= 1:
                    spositive += 1
                elif -0.5 < analysis.sentiment.polarity <= -0.2:
                    negative += 1
                elif -1 < analysis.sentiment.polarity <= -0.5:
                    snegative += 1

        # Write to csv and close file
        csvWriter.writerow(self.tweetText)
        csvFile.close()

        # Calculate percentages (using the actual number of tweets retrieved)
        actual_tweets = len(self.tweets.data) if self.tweets.data else 1
        positive = self.percentage(positive, actual_tweets)
        spositive = self.percentage(spositive, actual_tweets)
        negative = self.percentage(negative, actual_tweets)
        snegative = self.percentage(snegative, actual_tweets)
        neutral = self.percentage(neutral, actual_tweets)

        # Calculate average polarity
        polarity = polarity / actual_tweets if actual_tweets > 0 else 0

        # Determine overall sentiment for HTML display (same logic as before)
        if -0.2 < polarity <= 0.2:
            htmlpolarity = "Neutral"
        elif 0.2 < polarity <= 0.5:
            htmlpolarity = "Positivo"
        elif 0.5 < polarity <= 1:
            htmlpolarity = "Altamente Positivo"
        elif -0.5 < polarity <= -0.2:
            htmlpolarity = "Negativo"
        elif -1 < polarity <= -0.5:
            htmlpolarity = "Altamente Negativo"

        return polarity, htmlpolarity, positive, spositive, negative, snegative, neutral, keyword, actual_tweets

    # Resto de los métodos (cleanTweet, percentage, plotPieChart) permanecen igual
    def cleanTweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def percentage(self, part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')

# Las rutas sentiment_logic y visualize permanecen igual
@second.route('/sentiment_logic', methods=['POST', 'GET'])
def sentiment_logic():
    keyword = request.form.get('keyword')
    tweets = request.form.get('tweets')
    bear=request.form.get('bear')
    sa = SentimentAnalysis()
    
    polarity, htmlpolarity, positive,  spositive, negative,  snegative, neutral, keyword1, tweet1 = sa.DownloadData(
        keyword, tweets, bear)
    return render_template('sentiment_analyzer.html', polarity=polarity, htmlpolarity=htmlpolarity, positive=positive, spositive=spositive, negative=negative, snegative=snegative, neutral=neutral, keyword=keyword1, tweets=tweet1)