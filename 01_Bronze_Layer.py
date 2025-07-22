# Databricks notebook source
# Bibliotecas
import requests
import json
from datetime import datetime

# COMMAND ----------

# --- 1. Configuração ---
api_key = "SUA_CHAVE_API_OPENWEATHERMAP"
base_url = "https://api.openweathermap.org/data/2.5/weather?"

# Cidades de interesse
cities = {
    "SaoPaulo": {"lat": -23.5505, "lon": -46.6333},
    "RioDeJaneiro": {"lat": -22.9068, "lon": -43.1729},
    "Guarulhos": {"lat": -23.4632, "lon": -46.5369}
}

bronze_path = "/mnt/clima_data/bronze/raw_weather_data"

# COMMAND ----------

# --- 2. Coleta de Dados (API) e Armazenamento Temporário ---
all_weather_data = []

for city_name, coords in cities.items():
    lat = coords["lat"]
    lon = coords["lon"]
    url = f"{base_url}lat={lat}&lon={lon}&appid={api_key}&units=metric" # units=metric para Celsius

    try:
        response = requests.get(url)
        response.raise_for_status() # Lança exceção para erros HTTP
        data = response.json()
        data['city_name'] = city_name # Adiciona o nome da cidade para identificação
        data['ingestion_timestamp'] = datetime.now().isoformat() # Timestamp de ingestão
        all_weather_data.append(data)
    except requests.exceptions.RequestException as e:
        print(f"Erro ao coletar dados para {city_name}: {e}")

# --- 3. Armazenamento no Delta Lake (Bronze) ---
# Criar um DataFrame Spark a partir dos dados coletados
# Note: Spark inferirá o esquema, o que é útil para dados semi-estruturados na Bronze
df_bronze = spark.createDataFrame(all_weather_data)

# Salvar como tabela Delta na camada Bronze
df_bronze.write.format("delta").mode("append").save(bronze_path)

print(f"Dados brutos salvos na camada Bronze em: {bronze_path}")
print(f"Número de registros adicionados: {df_bronze.count()}")

# Opcional: Visualizar alguns dados
display(spark.read.format("delta").load(bronze_path))