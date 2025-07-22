# Databricks notebook source
# Bibliotecas
from pyspark.sql.functions import col, avg, date_trunc, count, mode, round

# --- 1. Configuração de Caminhos ---
silver_path = "/mnt/clima_data/silver/cleaned_weather_data"
gold_daily_summary_path = "/mnt/clima_data/gold/daily_weather_summary"

# --- 2. Leitura da Camada Silver ---
df_silver = spark.read.format("delta").load(silver_path)

# --- 3. Agregações para Camada Gold ---

# Exemplo 1: Sumário Diário por Cidade
df_gold_daily_summary = df_silver \
    .withColumn("observation_date", date_trunc("day", col("observation_timestamp_utc"))) \
    .groupBy("city_name", "country_code", "observation_date") \
    .agg(
        round(avg("temperature_celsius"), 2).alias("avg_temperature_celsius"),
        round(avg("feels_like_celsius"), 2).alias("avg_feels_like_celsius"),
        round(avg("humidity_percent"), 2).alias("avg_humidity_percent"),
        round(avg("wind_speed_mps"), 2).alias("avg_wind_speed_mps"),
        mode("weather_description").alias("most_common_weather_description"), # Descrição mais frequente
        count("*").alias("observation_count_daily")
    ) \
    .orderBy("city_name", "observation_date")

# --- 4. Armazenamento no Delta Lake (Gold) ---
# Para agregação diária, é comum usar overwrite por dia ou particionar
# Para este projeto, vamos usar "overwrite" se for um resumo que sempre recalcula tudo.
# Se for crescer, use "append" e gerencie duplicações.
df_gold_daily_summary.write.format("delta").mode("overwrite").save(gold_daily_summary_path)

print(f"Dados agregados diários salvos na camada Gold em: {gold_daily_summary_path}")
print(f"Número de registros agregados: {df_gold_daily_summary.count()}")

# Opcional: Visualizar alguns dados
display(spark.read.format("delta").load(gold_daily_summary_path))