# Projeto de Engenharia de Dados: Análise Climática com Databricks

Este repositório contém um projeto de Engenharia de Dados que demonstra a construção de um pipeline de dados utilizando o **Databricks Community Edition**. O projeto coleta dados climáticos públicos, os processa através das camadas Bronze, Silver e Gold (Medallion Architecture), e realiza análises descritivas.

---

## 🚀 Visão Geral do Projeto

O objetivo principal é simular um processo de ETL/ELT para dados climáticos, transformando dados brutos em insights acionáveis.

**Arquitetura de Dados:**
* **Bronze Layer (Raw):** Armazena os dados brutos e originais diretamente da fonte (API do OpenWeatherMap).
* **Silver Layer (Cleaned & Conformed):** Contém os dados limpos, padronizados e enriquecidos, prontos para análises mais aprofundadas.
* **Gold Layer (Curated & Aggregated):** Apresenta dados agregados e otimizados para consumo por aplicações de BI, dashboards e modelos de Machine Learning.

---

## 📊 Fonte de Dados

Os dados climáticos são coletados em tempo real (ou próximo a tempo real) da **OpenWeatherMap API**.

* **API Utilizada:** [https://openweathermap.org/api](https://openweathermap.org/api)
* **Para usar a API, é necessário registrar-se e obter uma API Key gratuita:** [https://home.openweathermap.org/users/sign_up](https://home.openweathermap.org/users/sign_up)

---

## 🛠️ Tecnologias Utilizadas

* **Databricks Community Edition:** Plataforma de Data & AI para execução de notebooks Spark.
* **Apache Spark (PySpark):** Para processamento distribuído de dados.
* **Delta Lake:** Formato de armazenamento de dados open-source para construir Data Lakes confiáveis e escaláveis.
* **Python:** Linguagem de programação para scripts e transformações.
* **`requests`:** Biblioteca Python para consumir APIs REST.
* **`matplotlib` & `seaborn`:** Bibliotecas Python para visualização de dados (usadas nas análises descritivas).

---

## 📁 Estrutura do Repositório

databricks-climate-project-pipeline/
├── notebooks/
│   ├── 01_Bronze_Layer.ipynb              # Coleta e ingestão de dados brutos na camada Bronze.
│   ├── 02_Silver_Layer.ipynb              # Limpeza, padronização e transformação de dados para a camada Silver.
│   ├── 03_Gold_Layer.ipynb                # Agregação e otimização de dados para a camada Gold.
│   └── 04_Descriptive_Analysis.ipynb      # Realiza análises descritivas e visualizações dos dados.
└── README.md                              # Este arquivo.

---

## 🚀 Como Executar o Projeto

Siga os passos abaixo para configurar e executar este projeto no Databricks Community Edition:

### Pré-requisitos:

1.  **Conta Databricks Community Edition:** Crie uma conta gratuita em [https://community.cloud.databricks.com/](https://community.cloud.databricks.com/).
2.  **Cluster Spark:** No seu workspace Databricks, crie um cluster. Para a Community Edition, um cluster padrão (e.g., versão `14.3 LTS (Scala 2.12, Spark 3.5.0)`) com configuração mínima é suficiente.
3.  **OpenWeatherMap API Key:** Obtenha sua chave de API conforme instruções na seção "Fonte de Dados".

### Passos de Execução:

1.  **Configurar a API Key:**
    * Abra o notebook `01_Bronze_Layer.ipynb`.
    * Localize a linha `api_key = "SUA_CHAVE_API_OPENWEATHERMAP"` e substitua `"SUA_CHAVE_API_OPENWEATHERMAP"` pela sua chave de API real do OpenWeatherMap. **Não comite sua chave de API diretamente no GitHub!** Use Databricks Secrets para produção, mas para este projeto de estudo, pode deixá-la no código para fins didáticos (com o cuidado de não subir para repositórios públicos).

2.  **Executar os Notebooks em Ordem:**
    * Anexe cada notebook ao cluster que você criou.
    * Execute os notebooks na seguinte ordem:
        1.  `01_Bronze_Layer.ipynb`
        2.  `02_Silver_Layer.ipynb`
        3.  `03_Gold_Layer.ipynb`
        4.  `04_Descriptive_Analysis.ipynb`

    Certifique-se de que cada notebook seja executado com sucesso antes de passar para o próximo. Eles criarão e popularão as tabelas Delta nas camadas correspondentes no DBFS.

---

## 📊 Análises Descritivas

O notebook `04_Descriptive_Analysis.ipynb` apresenta exemplos de como consultar e analisar os dados processados na camada Gold. Você encontrará:

* Estatísticas básicas de temperatura, umidade e velocidade do vento.
* Tendências temporais de temperatura para cidades específicas.
* Distribuição da umidade.
* Identificação das condições climáticas mais comuns.

Sinta-se à vontade para expandir essas análises e criar mais visualizações!

---

**Desenvolvido por: Guilherme Noronha - github.com/guinnoronha**
