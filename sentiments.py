from flask import Blueprint, render_template, request
import matplotlib.pyplot as plt
import os
import tweepy
import csv
import re
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
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
        # Creating variables to store sentiment info
        polarity = 0
        positive = 0
        negative = 0
        neutral = 0
        analysis = 0
        sia = SentimentIntensityAnalyzer()
        # Authenticating with Bearer Token (API v2)
        bearer_token = bear # Reemplaza con tu Bearer Token real
        client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)

        # convertir la cantidad de tweets a un entero
        tweets = int(tweets)
        
        # Nota: La API v2 tiene límites diferentes en la cantidad de tweets que puedes obtener
        self.tweets = client.search_recent_tweets(
            query=keyword,
            max_results=tweets if tweets <= 100 else 100,  # Máximo 100 tweets en el plan básico
            tweet_fields=['created_at', 'text']
        )

        # Open/create a file to append data to
        csvFile = open('result.csv', 'a')
        csvWriter = csv.writer(csvFile)
        
        # Iterating through tweets fetched
        if self.tweets.data:
            for tweet in self.tweets.data:
                # Append cleaned tweet text to list
                self.tweetText.append(self.cleanTweet(tweet.text).encode('utf-8'))
                
                analysis = sia.polarity_scores(tweet.text)
                
                compound=analysis['compound']
                polarity += compound
                
                # Categorize sentiment (same logic as before)
                if -0.2 < compound <= 0.2:
                    neutral += 1
                elif 0.2 < compound <= 1:
                    positive += 1
                elif -1 < compound <= -0.2:
                    negative += 1

        # Write to csv and close file
        csvWriter.writerow(self.tweetText)
        csvFile.close()
        # Calculate percentages (using the actual number of tweets retrieved)
        actual_tweets = len(self.tweets.data) if self.tweets.data else 1
        positive = self.percentage(positive, actual_tweets)
        negative = self.percentage(negative, actual_tweets)
        neutral = self.percentage(neutral, actual_tweets)

        # Calcula el porcentaje de la polaridad total
        polarity = polarity / actual_tweets if actual_tweets > 0 else 0

        # Calcular el sentimiento general para visualización en HTML (con la misma lógica anterior)
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

        return polarity, htmlpolarity, positive, negative, neutral, keyword, actual_tweets

    # Resto de los métodos (cleanTweet, percentage, plotPieChart) permanecen igual
    def cleanTweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def percentage(self, part, whole):
        temp = (float(part) / float(whole))* 100
        return format(temp, '.2f')

# Las rutas sentiment_logic y visualize permanecen igual
@second.route('/sentiment_logic', methods=['POST', 'GET'])
def sentiment_logic():
    keyword = request.form.get('keyword')
    tweets = request.form.get('tweets')
    bear=request.form.get('bear')
    sa = SentimentAnalysis()
    
    polarity, htmlpolarity, positive, negative, neutral, keyword1, tweet1 = sa.DownloadData(
        keyword, tweets, bear)
    polarity = round(polarity, 3)
    return render_template('sentiment_analyzer.html', polarity=polarity,htmlpolarity=htmlpolarity, positive=positive, negative=negative,
    neutral=neutral, keyword=keyword1, tweets=tweet1)
