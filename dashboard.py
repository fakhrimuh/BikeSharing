# Library Manipulasi Data
import streamlit as st
import numpy as np
import pandas as pd

# import VIsualisasi Data
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error

path_day_dataset = "https://raw.githubusercontent.com/fakhrimuh/BikeSharing/main/day.csv"


st.header("Bike Sharing ")

    # Konten lainnya
st.write("Aplikasi streamlit ini dibuat untuk menjawab pertanyaan berikut")
st.markdown("- Apakah kondisi cuaca, seperti suhu, kelembapan, atau kecepatan angin, memiliki pengaruh terhadap tingkat penyewaan sepeda? Apakah ada korelasi antara kondisi cuaca tertentu dengan jumlah penggunaan sepeda")
st.markdown("- Bagaimana perbedaan penyewaan sepeda antara hari libur dan hari kerja ini dapat mempengaruhi strategi pemasaran atau operasional terkait dengan penyediaan sepeda selama hari libur dan hari kerja")

"""## Data Wrangling

### Gathering Data
"""

#memanggil dataset
day_df = pd.read_csv(path_day_dataset)

st.dataframe(day_df)

# ...

st.subheader("Assessing Data")

# Menampilkan statistik deskriptif
st.subheader("Descriptive Statistics")
st.write(day_df.describe())

# Menampilkan jumlah data duplikat
st.subheader("Duplicate Data")
st.write("Jumlah data duplikat pada data per hari:", day_df[day_df.duplicated()].shape[0])

# Membagi layar menjadi dua kolom
col1, col2 = st.columns(2)

# Menampilkan tabel pertama pada kolom pertama
with col1:
    # Menampilkan jumlah missing value per kolom
    st.subheader("Missing Values")
    st.write("Jumlah Missing Value per Kolom pada data per hari:")
    st.write(day_df.isnull().sum())

# Menampilkan tabel kedua pada kolom kedua
with col2:
    st.subheader("Data Types")
    st.write("Tipe Data: ")
    st.write(day_df.dtypes)

# Membersihkan data dan menampilkan informasi setelah pembersihan
st.subheader("Cleaning Data")
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
st.write("Jumlah Data Yang Hilang: ", day_df.info())

# Pertanyaan 1: Pengaruh cuaca
st.title("Analisis Data: Bike Sharing")
st.header("Pertanyaan 1: Pengaruh Cuaca")
st.write("Analisis deskriptif, tren, dan korelasi antar variabel cuaca.")

# Menampilkan korelasi
# Membuat matriks korelasi
correlation_matrix = day_df[['temp', 'hum', 'windspeed', 'cnt']].corr()

# Menampilkan heatmap dengan Seaborn
sns.set(style="white")
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=.5)

# Menyimpan plot ke variabel
heatmap_plot = plt.gcf()

# Menampilkan plot menggunakan st.pyplot() dengan argumen
st.pyplot(heatmap_plot)

st.write("Cuaca memiliki pengaruh besar terhadap jumlah pengguna rental sepeda dan musim dengan paling banyak penggunanya adalah musim panas dan musim gugur")


day_df['total_rentals'] = day_df['casual'] + day_df['registered']
rentals_per_season = day_df.groupby('season')['total_rentals'].sum().reset_index()

# Mengubah label musim dari angka menjadi teks
season_dict = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
rentals_per_season['season'] = rentals_per_season['season'].map(season_dict)


# Visualisasi data dengan Streamlit
st.markdown("### Jumlah Total Penyewa Sepeda per Musim")
st.bar_chart(rentals_per_season.set_index('season')['total_rentals'])
# ...

# Perbedaan penyewaan sepeda antara hari libur dan hari kerja
st.header("Perbedaan Penyewaan Sepeda")
st.write("Analisis perbedaan penyewaan sepeda antara hari libur dan hari kerja.")

# Menampilkan bar chart perbedaan rata-rata
st.subheader("Rata-Rata Penyewaan Sepeda pada Hari Libur dan Hari Kerja")
avg_rentals_holiday = day_df[day_df['holiday'] == 1]['cnt'].mean()
avg_rentals_workingday = day_df[day_df['workingday'] == 1]['cnt'].mean()

bars = st.bar_chart({'Hari Libur': avg_rentals_holiday, 'Hari Kerja': avg_rentals_workingday})

# Menambahkan selisih persentase dalam print statement
percentage_difference = ((avg_rentals_workingday - avg_rentals_holiday) / avg_rentals_workingday) * 100
st.write(f'Selisih persentase rata-rata penyewaan sepeda pada hari libur dan hari kerja: {round(percentage_difference, 2)}%')


st.subheader("Conclusion")

"""
Apakah kondisi cuaca, seperti suhu, kelembapan, atau kecepatan angin, memiliki pengaruh terhadap tingkat penyewaan sepeda? Apakah ada korelasi antara kondisi cuaca tertentu dengan jumlah penggunaan sepeda


*   diantara variabel berhubungan dengan cuaca yang paling besar pengaruhnya adalah variabel suhu sebesar 63%
*   Cuaca memiliki faktor yang besar untuk pengaruh jumlah pengguna rental sepeda
"""

"""
####Bagaimana perbedaan penyewaan sepeda antara hari libur dan hari kerja ini dapat mempengaruhi strategi pemasaran atau operasional terkait dengan penyediaan sepeda selama hari libur dan hari kerja


*   Penyewa Sepeda menggunakan sepeda lebih banyak pada hari kerja dibandingkan dengan hari libur
*   Dapat Menjadi Acuan jika ingin melakukan promosi dengan menargetkan kepada para pekerja atau anak sekolah yang menyewa sepeda
"""