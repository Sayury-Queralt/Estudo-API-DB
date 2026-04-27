from dotenv import load_dotenv
import os
import urllib.request
import json
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo
import psycopg2
import boto3

load_dotenv()
API_KEY = os.getenv('API_GNews')
host_RDS = os.getenv('HOST')
region = os.getenv('region')
database = os.getenv('database')
user = os.getenv('user')
sslmode = os.getenv('sslmode')

Tema = "Lula"
LastHour = (datetime.now(timezone.utc) - timedelta(hours=24)).strftime('%Y-%m-%dT%H:%M:%SZ')

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


def Conexao_DB(host_RDS, region, database, user, sslmode):
    client = boto3.client('rds', region_name=region)
    auth_token = client.generate_db_auth_token(
        DBHostname=host_RDS,
        Port=5432,
        DBUsername = user,
        Region=region
    )

    conn = None
    try:
        conn = psycopg2.connect(
            host = host_RDS,
            port=5432,
            database=database,
            user=user,
            password=auth_token,
            sslmode=sslmode
        )
        return conn
    except Exception as e:
        print(f"Database error: {e}")
        return None

def Criar_Tabela(conn):
    """Cria a tabela caso ela não exista no banco"""
    try:
        cur = conn.cursor()
        # O comando IF NOT EXISTS evita erros se a tabela já existir
        query_create = """
        CREATE TABLE IF NOT EXISTS noticias (
            ID SERIAL PRIMARY KEY,
            Titulo TEXT,
            Descricao TEXT,
            Topico TEXT,
            Data TIMESTAMP,
            Fonte TEXT,
            url TEXT
        );
        """
        cur.execute(query_create)
        conn.commit()
        cur.close()
        print("Verificação de tabela concluída (OK).")
    except Exception as e:
        print(f"Erro ao criar tabela: {e}")
    
def Upload_DB(articles, Tema):
    conn = Conexao_DB(host_RDS, region, database, user, sslmode)
    if not conn:
        return
    
    Criar_Tabela(conn)
    
    try:
        cur = conn.cursor()
        
        # Exemplo de query para suas notícias da GNews
        query = "INSERT INTO noticias (Titulo, Descricao, Topico, Data, Fonte, url) VALUES (%s, %s, %s, %s, %s, %s)"
        
        for item in articles:
            Completo = item[:2] + (Tema,) + item[2:]
            cur.execute(query, Completo)
        
        conn.commit()
        print(f"Sucesso! {len(articles)} registros enviados.")
        
        cur.close()
    except Exception as e:
        print(f"Erro durante o upload: {e}")
    finally:
        if conn:
            conn.close()

# --- Execução ---
if __name__ == "__main__":
    artigos = GET_Article(url)
    if artigos:
        dados = Montagem_dados(artigos)
        Upload_DB(dados, Tema)