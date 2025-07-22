# Databricks notebook source
# Bibliotecas
import matplotlib.pyplot as plt
import seaborn as sns
from pyspark.sql.functions import col, min, max, avg, stddev, percentile_approx, round, mode # <-- Add round here!

# --- 1. Configuração de Caminhos ---
gold_daily_summary_path = "/mnt/clima_data/gold/daily_weather_summary"
silver_path = "/mnt/clima_data/silver/cleaned_weather_data" # Para análises mais granulares

# --- 2. Leitura da Camada Gold (e Silver, se necessário) ---
df_gold_daily = spark.read.format("delta").load(gold_daily_summary_path)
df_silver = spark.read.format("delta").load(silver_path) # Para análises por hora/minuto

# Converter para Pandas DataFrame para visualização (se o dataset for gerenciável na memória do driver)
# Para datasets grandes, use as visualizações built-in do Databricks ou bibliotecas como Plotly com Spark.
# Certifique-se de que o DataFrame não está vazio antes de converter para Pandas
if df_gold_daily.count() > 0:
    df_gold_pandas = df_gold_daily.toPandas()
else:
    df_gold_pandas = None # Ou um DataFrame Pandas vazio, para evitar erros posteriores

# --- 3. Análises Descritivas ---

print("--- Estatísticas Gerais da Temperatura Diária Média (Celsius) ---")
# Use the 'round' function from pyspark.sql.functions
df_gold_daily.select(
    round(avg("avg_temperature_celsius"), 2).alias("Media_Temp_Celsius"),
    round(stddev("avg_temperature_celsius"), 2).alias("Desvio_Padrao_Temp_Celsius"),
    round(min("avg_temperature_celsius"), 2).alias("Min_Temp_Celsius"),
    round(max("avg_temperature_celsius"), 2).alias("Max_Temp_Celsius")
).show()

print("\n--- Temperatura Média Diária por Cidade ---")
df_gold_daily.groupBy("city_name") \
    .agg(round(avg("avg_temperature_celsius"), 2).alias("Temperatura_Media_Historica_Celsius")) \
    .show()

# Exemplo de Visualização: Tendência de Temperatura ao longo do tempo para uma cidade específica
if df_gold_pandas is not None and not df_gold_pandas.empty:
    city_to_plot = "SaoPaulo"
    df_sp = df_gold_pandas[df_gold_pandas['city_name'] == city_to_plot].sort_values('observation_date')

    if not df_sp.empty:
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=df_sp, x='observation_date', y='avg_temperature_celsius')
        plt.title(f'Tendência de Temperatura Média Diária em {city_to_plot}')
        plt.xlabel('Data de Observação')
        plt.ylabel('Temperatura Média (°C)')
        plt.grid(True)
        plt.show()
    else:
        print(f"Não há dados para {city_to_plot} para plotagem.")
else:
    print("DataFrame Pandas vazio ou nulo para visualização. Verifique a camada Gold.")


# Exemplo: Distribuição de Umidade para todas as cidades
print("\n--- Distribuição de Umidade ---")
if df_gold_pandas is not None and not df_gold_pandas.empty:
    plt.figure(figsize=(10, 6))
    sns.histplot(df_gold_pandas['avg_humidity_percent'], bins=15, kde=True)
    plt.title('Distribuição da Umidade Média Diária')
    plt.xlabel('Umidade Média (%)')
    plt.ylabel('Frequência')
    plt.grid(True)
    plt.show()
else:
    print("DataFrame Pandas vazio ou nulo para visualização de umidade. Verifique a camada Gold.")

# Exemplo: Condição Climática Mais Comum por Cidade
print("\n--- Condição Climática Mais Comum por Cidade ---")
df_gold_daily.groupBy("city_name") \
    .agg(mode("most_common_weather_description").alias("Condicao_Mais_Comum")) \
    .show(truncate=False)