import streamlit as st
import requests
import pandas as pd
from pyspark.sql import SparkSession
import plotly.express as px

def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd'
    }
    response = requests.get(url, params=params)
    data = response.json()
    return pd.DataFrame(data)

st.title("Crypto Market Analytics Dashboard")

spark = SparkSession.builder.appName("CryptoAnalytics").getOrCreate()

df_pd = fetch_crypto_data()
df_spark = spark.createDataFrame(df_pd)
df_spark.createOrReplaceTempView("cryptos_temp")

limit = st.select_slider("Select the number of top coins to display:", options=range(1, df_spark.count() + 1), value=10)

top_coin = df_spark.select("id", "symbol", "name", "price_change_percentage_24h") \
    .orderBy(df_spark["price_change_percentage_24h"].desc()) \
    .limit(limit)


st.write("Top "+str(limit)+" Coin(s) in Last (24h)")
st.dataframe(top_coin.toPandas())

fig = px.bar(top_coin.toPandas(), x='name', y='price_change_percentage_24h', color='name')
st.plotly_chart(fig)