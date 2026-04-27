from dotenv import load_dotenv
import os
import urllib.request
import json
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo
import psycopg2

load_dotenv()
API_KEY = os.getenv('API_GNews')

Tema = input('Buscar noticias com a palavra: ')
LastHour = (datetime.now(timezone.utc) - timedelta(hours=15)).strftime('%Y-%m-%dT%H:%M:%SZ')

url = f"https://gnews.io/api/v4/search?q={Tema}&country=br&from={LastHour}&lang=pt&max=100&apikey={API_KEY}"

def GET_Article(url):
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode("utf-8"))
            articles = data.get("articles", [])
            return articles
        
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return []

def Montagem_dados(articles):
    df_article = [(
        article.get('title'),
        article.get('description'),
        article.get('publishedAt'),
        article.get('source', {}).get('name'),
        article.get('source', {}).get('url'))
        for article in articles
    ]
    return df_article


df_articles = GET_Article(url)
df_articles = Montagem_dados(df_articles)
print(df_articles)



def Conexao_DB():
    connection = psycopg2.connect(
        user="postgres",
        password="p0stgres123",
        host="127.0.0.1", 
        port="5432",
        database="postgres",
        connect_timeout=5  
    )

def Upload_DB(articles):
    Conexao_DB()
    for article in articles:

        print(f"Título: {article['title']}")
        print(f"Descrição: {article.get('description', 'Sem descrição disponível')}")
        print(f"Data: {datetime.fromisoformat(article['publishedAt'])}")
        print(f"Fonte: {article['source']['name']} | url: {article['source']['url']}")
        print("-" * 30)
        #for article in articles:
        #    print("--- Novas informações encontradas ---")
        #    for chave, valor in article.items():
        #        print(f"{chave}: {valor}")
        #    break
