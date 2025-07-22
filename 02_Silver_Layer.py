# Databricks notebook source
# Bibliotecas
from pyspark.sql.functions import col, from_unixtime, to_timestamp, explode # Remova get_json_object

# --- 1. Configuração de Caminhos ---
bronze_path = "/mnt/clima_data/bronze/raw_weather_data"
silver_path = "/mnt/clima_data/silver/cleaned_weather_data"

# --- 2. Leitura da Camada Bronze ---
df_bronze = spark.read.format("delta").load(bronze_path)

# Verifique o schema para entender as colunas (execute isso e olhe a saída)
df_bronze.printSchema()

# --- 3. Transformações para Camada Silver ---
df_silver = df_bronze.select(
    col("city_name"),
    col("ingestion_timestamp"),
    from_unixtime(col("dt")).alias("observation_timestamp_utc"),
    # Acesso direto aos campos do MAP/STRUCT:
    col("main.temp").cast("float").alias("temperature_celsius"),
    col("main.feels_like").cast("float").alias("feels_like_celsius"),
    col("main.humidity").cast("integer").alias("humidity_percent"),
    col("wind.speed").cast("float").alias("wind_speed_mps"),
    col("sys.country").alias("country_code"),
    col("coord.lat").cast("float").alias("latitude"),
    col("coord.lon").cast("float").alias("longitude"),
    explode(col("weather")).alias("weather_info") # explode o array 'weather'
).select(
    col("city_name"),
    col("ingestion_timestamp"),
    col("observation_timestamp_utc"),
    col("temperature_celsius"),
    col("feels_like_celsius"),
    col("humidity_percent"),
    col("wind_speed_mps"),
    col("country_code"),
    col("latitude"),
    col("longitude"),
    col("weather_info.description").alias("weather_description"),
    col("weather_info.main").alias("weather_main_category")
)

# Convertendo para tipo Timestamp adequado para análise de tempo
df_silver = df_silver.withColumn("observation_timestamp_utc", to_timestamp(col("observation_timestamp_utc")))
df_silver = df_silver.withColumn("ingestion_timestamp", to_timestamp(col("ingestion_timestamp")))


# --- 4. Armazenamento no Delta Lake (Silver) ---
df_silver.write.format("delta").mode("append").save(silver_path)

print(f"Dados limpos e padronizados salvos na camada Silver em: {silver_path}")
print(f"Número de registros adicionados: {df_silver.count()}")

# Opcional: Visualizar alguns dados
display(spark.read.format("delta").load(silver_path))