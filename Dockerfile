# Imagem oficial do Python leve
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /API-GNews

# Copia o arquivo de dependências para o container
COPY requirements.txt .

# Instala as bibliotecas (ex: requests, psycopg2-binary)
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o conteúdo da sua pasta local para o container
COPY . .

# Comando para rodar o script
CMD ["python", "GET_API_GNews.py"]