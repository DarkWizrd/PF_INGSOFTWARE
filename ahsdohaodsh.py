import pandas as pd
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

sentimientos=SentimentIntensityAnalyzer()

str ="i love so much mr robot :c !"
str2=sentimientos.polarity_scores(str)
print(str2['compound'])
print(str2['pos'])
print(-1*str2['neu'])
print(str2['neg'])
