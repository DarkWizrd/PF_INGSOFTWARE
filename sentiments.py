from flask import Blueprint, render_template, request
import matplotlib.pyplot as plt
import os
import tweepy
import math
import csv
import re
from textblob import TextBlob
import pandas as pd
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

    def DownloadData(self, keyword, tweets, bear):
        # Validar entrada
        if not bear or not keyword or not tweets:
            return 0, "Datos inválidos", 0, 0, 0, keyword, 0

        try:
            tweets = int(tweets)
            if tweets <= 0:
                return 0, "Número inválido", 0, 0, 0, keyword, 0
        except ValueError:
            return 0, "Número inválido", 0, 0, 0, keyword, 0

        # Inicializar variables
        polarity = 0
        positive = 0
        negative = 0
        neutral = 0
        sia = SentimentIntensityAnalyzer()

        try:
            # Autenticación
            client = tweepy.Client(bearer_token=bear, wait_on_rate_limit=True)
            
            # Búsqueda de tweets
            self.tweets = client.search_recent_tweets(
                query=keyword,
                max_results=min(tweets, 100),  # Máximo 100 tweets
                tweet_fields=['created_at', 'text'],
                user_fields=['profile_image_url'],
                expansions=['author_id']
            )
        except tweepy.TweepyException as e:
            print(f"Error de API: {e}")
            return 0, "Error de API", 0, 0, 0, keyword, 0

        # Procesar tweets
        if not self.tweets.data:
            return 0, "Sin resultados", 0, 0, 0, keyword, 0

        # Escribir en CSV
        with open('result.csv', 'w', newline='', encoding='utf-8') as csvFile:
            csvWriter = csv.writer(csvFile)
            for tweet in self.tweets.data:
                cleaned_tweet = self.cleanTweet(tweet.text)
                self.tweetText.append(cleaned_tweet)
                csvWriter.writerow([cleaned_tweet])
                
                analysis = sia.polarity_scores(tweet.text)
                compound = analysis['compound']
                polarity += compound
                
                # Categorizar sentimiento
                if -0.1 < compound <= 0.1:
                    neutral += 1
                elif compound > 0.1:
                    positive += 1
                else:
                    negative += 1

        # Calcular métricas
        actual_tweets = len(self.tweets.data)
        positive_pct = self.percentage(positive, actual_tweets)
        negative_pct = self.percentage(negative, actual_tweets)
        neutral_pct = self.percentage(neutral, actual_tweets)
        avg_polarity = polarity / actual_tweets if actual_tweets > 0 else 0
        avg_polarity = math.trunc(avg_polarity * 1000) / 1000  # Redondear a 3 decimales

        # Determinar sentimiento general
        if -0.1 < avg_polarity <= 0.1:
            htmlpolarity = "Neutral"
        elif avg_polarity > 0.1:
            htmlpolarity = "Positivo"
        else:
            htmlpolarity = "Negativo"

        return avg_polarity, htmlpolarity, positive_pct, negative_pct, neutral_pct, keyword, actual_tweets

    def cleanTweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def percentage(self, part, whole):
        return format((float(part) / float(whole)) * 100, '.2f') if whole != 0 else 0

@second.route('/sentiment_logic', methods=['POST'])
def sentiment_logic():
    keyword = request.form.get('keyword', '').strip()
    tweets = request.form.get('tweets', '10').strip()
    bear = request.form.get('bear', '').strip()
    
    sa = SentimentAnalysis()
    results = sa.DownloadData(keyword, tweets, bear)
    
    if len(results) == 7:
        polarity, htmlpolarity, positive, negative, neutral, keyword, tweet_count = results
        return render_template(
            'sentiment_analyzer.html',
            polarity=polarity,
            htmlpolarity=htmlpolarity,
            positive=positive,
            negative=negative,
            neutral=neutral,
            keyword=keyword,
            tweets=tweet_count
        )
    else:
        return render_template(
            'sentiment_analyzer.html',
            error=results[1] if len(results) > 1 else "Error desconocido"
        )