import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


st.header("Dicoding-Bangkit-Air Quality Analysis")
st.write("Dikerjakan oleh Axelliano Rafael Situmeang - Bangkit ID : m200d4ky1918 - Dicoding ID : lyfora")
st.write("Data Diperoleh dari :https://drive.google.com/file/d/1RhU3gJlkteaAQfyn9XOVAz7a5o1-etgr/view")


st.subheader("Pengenalan Data")
st.write('Data terdiri atas berbagai feature komponen udara seperti kelompok Polutan (SO2,NO2,CO2), Ozon, Temperature dan lain-lain')
st.write("Disini kita akan memberikan hasil analisis yang kami olah")
# Subheader Antar Variabel
st.subheader("Hubungan antar Variabel")

# Fetching Data
merged_df = pd.read_csv("merged_asli_data.csv")
merged_df.fillna(method='ffill', inplace=True)
# Buang Yang Ga penting
df_valuable = merged_df.iloc[:, 5:]
object_cols = merged_df.select_dtypes(include=['object']).columns
object_cols = [col for col in object_cols if col != 'station']

# Untuk GroupBy
merged_df_1 = merged_df.drop(columns=object_cols)

# Untuk DF_Coor
df_valuable = df_valuable.select_dtypes(exclude=['object'])
merged_df_coor = df_valuable.corr()
fig = plt.figure(figsize=(10, 8))
sns.heatmap(merged_df_coor, annot=True, fmt=".2f",
            cmap='coolwarm', cbar=True, square=True)
plt.title('Heatmap of Correlation Matrix Air Quality')
st.pyplot(fig)
with st.container():
    st.markdown("""
    <div style="padding: 10px; margin: 10px; border: 1px solid #CCC;">
        <h3>Didapati bahwa ada 2 grup yang cukup mencolok yakni:</h3>
        <ul>
            <li>Group 1 - Kualitas Udara secara Kimia (PM2.5 PM.10 SO2 NO2 CO)</li>
            <li>Group 2 - Kualitas Udara secara Fisika (O3, TEMP, PRES, DEWP)</li>
        </ul>
        <p>Secara Kimiawi, Partikel NO2, SO2, CO cukup berbahaya dikarenakan ada kemungkinan beberapa partikel lebih kecil dari 2.5 dan 10 mikron. Menariknya adalah, Ada kaitan kecil antara kenaikan SO2, dan CO, terhadap penurunan Temperatur</p>
        <p>Disisi lain, benar bahwa Ozon memegang peranan penting untuk penjagaan temperatur yang mana, Ozon ini akan cenderung berkurang seiring dengan naiknya kadar NO2 (bisa dilihat terdapat correlation score moderat negatif antara O3 dan NO2)</p>
    </div>
    """, unsafe_allow_html=True)
# code = """def hello():
#     print("Hello, Streamlit!")"""
# st.code(code, language='python')
st.subheader("Grafik Polutan Udara tiap tahun")

# st.dataframe(data=merged_df, width=500, height=150)
grouped_df = merged_df_1.groupby(['station', 'year']).mean(
)[['PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'TEMP', 'O3']]
grouped_df.sort_values(by=['station', 'year'], inplace=True)
for pollutant in ['NO2', 'SO2', 'CO', 'TEMP', 'O3']:
    grouped_df[f'{pollutant}_pct_change'] = grouped_df.groupby(
        'station')[pollutant].transform(lambda x: x.pct_change()) * 100
# st.dataframe(data=grouped_df, width=500, height=150)
grouped_df = grouped_df.reset_index()

st.write('Polutan NO2')
fig = plt.figure(figsize=(12, 6))
sns.lineplot(data=grouped_df, x='year', y='NO2', hue='station', marker='o')
plt.title('NO2 Levels by Station Over Years')
plt.xlabel('Year')
plt.ylabel('NO2 Level')
st.pyplot(fig)

st.write('Polutan SO2')
fig = plt.figure(figsize=(12, 6))
sns.lineplot(data=grouped_df, x='year', y='SO2', hue='station', marker='o')
plt.title('SO2 Levels by Station Over Years')
plt.xlabel('Year')
plt.ylabel('SO2 Level')
st.pyplot(fig)

st.write('Polutan CO')
fig = plt.figure(figsize=(12, 6))
sns.lineplot(data=grouped_df, x='year', y='CO', hue='station', marker='o')
plt.title('CO Levels by Station Over Years')
plt.xlabel('Year')
plt.ylabel('CO Level')
st.pyplot(fig)

with st.container():
    st.markdown("""
        ## Analisis Kualitas Udara

        **1. Bagaimana perkembangan kualitas udara di beberapa lokasi dari tahun ke tahun?**

        Perkembangannya sangat fluktuatif dan secara garis besar dapat dikatakan stagnan dikarenakan kualitas udara dari tahun 2013 pada akhirnya tidak jauh berbeda dengan tahun 2017. 

        Tahun 2016 menjadi tahun dengan kualitas udara terbaik dengan data menunjukkan penurunan kadar SO2 minimal sebanyak 23% dari tahun sebelumnya di berbagai kota.
        Prestasi ini ternyata tidak bertahan lama sebelum akhirnya terjadi penurunan kualitas udara secara masif di tahun 2017 karena faktor ekonomi.

        **2. Apakah Polutan memengaruhi Suhu?**

        Dari Correlation Matrix pada Exploratory Analysis, data menunjukkan kadar SO2, NO2, dan CO yang merupakan polutan, memiliki andil kecil (-0.3 score) dalam pengaruhnya terhadap suhu. Adapun lebih lanjut, semakin naiknya polutan memicu penurunan suhu (negative correlation).
        Faktor paling utama tetap dipegang oleh Ozon (O3).

        **3. Bagaimana pengaruh Polutan terhadap Ozon (O3)?**

        Polutan khususnya NO2 sangat berpengaruh terhadap Ozon. Adapun dari data tahun ke tahun, lapisan ozon lebih mengarah ke negatif yang mana juga akan memicu pertumbuhan temperatur dan lain-lain.
    """, unsafe_allow_html=True)
