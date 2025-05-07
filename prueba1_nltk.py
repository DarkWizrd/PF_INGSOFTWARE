import pandas as pd
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

sentimientos=SentimentIntensityAnalyzer()

data = {
  "id": [1, 2, 3, 4, 5, 6],
  "texto": ["no me gusta esa camisa",
            "i hate fake news 😡",
            "que horrible es esa persona",
            "¡perfecto! :D",
            "Recoge la diversión, Que viene con ternura.",
            "i hate the fucking moty python"]
}

df = pd.DataFrame(data)

# imprimir comentarios
for i, row in df.iterrows():
  text=row['texto']
  myid=row['id']
  print(myid,text)


# puntuaciones de los sentimientos
for i, row in df.iterrows():
  text=row['texto']
  myid=row['id']
  resp=sentimientos.polarity_scores(text)
  df1=pd.DataFrame(resp, columns=['neg', 'neu', 'pos', 'compound'], index=[myid])
  print(df1)

# Clasificar comentarios usando compound

positivos=0
neutros=0
negativos=0
lpos=[]
lneg=[]
lneu=[]
for i, row in df.iterrows():
  text=row['texto']
  resp=sentimientos.polarity_scores(text)
  if resp['compound'] <= -0.05:
    lneg.append(text)
    negativos+=1
  elif resp['compound'] >= 0.05:#positivos
    positivos+=1
    lpos.append(text)
  elif -0.05 < resp['compound'] < 0.05:#neutros
    neutros+=1
    lneu.append(text)
  
  
print(f"\n+ Los comentarios que tienen tendencia a positivos son: {positivos}")
for elemento in lpos:
  print(elemento)
print(f"~ Los comentarios que tienen tendencia a neutros son: {neutros}")
for elemento in lneu:
  print(elemento)
print(f"- Los comentarios que tienen tendencia a negativos son: {negativos}")
for elemento in lneg:
    print(elemento)
  
