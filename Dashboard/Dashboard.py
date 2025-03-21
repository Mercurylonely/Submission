import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Supaya grafik tampil lebih baik di Streamlit
sns.set(style="whitegrid")
plt.rcParams.update({'figure.max_open_warning': 0})

st.title("Dashboard Analisis Penyewaan Sepeda")

st.markdown("""
Dashboard ini menyajikan insight mengenai:
- **Pengaruh Cuaca dan Musim** terhadap jumlah penyewaan sepeda.
- **Perbedaan Pola Penyewaan** antara hari kerja dan hari libur, terutama pada jam-jam tertentu.
""")

# ---- BAGIAN 1: DATA AGREGASI HARIAN ----
@st.cache_data
def load_merged_daily_data():
    # Pastikan file merged_daily_data.csv ada di direktori yang sama
    merged_daily = pd.read_csv("Dashboard/all_data.csv")
    merged_daily['dteday'] = pd.to_datetime(merged_daily['dteday'])
    # Buat kolom season_name dari kolom 'season'
    season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    merged_daily['season_name'] = merged_daily['season'].map(season_mapping)
    return merged_daily

merged_daily = load_merged_daily_data()

st.header("1. Pengaruh Cuaca dan Musim")
st.subheader("Rata-rata Penyewaan Sepeda per Musim")
avg_season = merged_daily.groupby('season_name')['cnt'].mean().reindex(['Spring','Summer','Fall','Winter'])

fig1, ax1 = plt.subplots(figsize=(8,5))
sns.barplot(x=avg_season.index, y=avg_season.values, palette="coolwarm", ax=ax1)
ax1.set_xlabel("Musim")
ax1.set_ylabel("Rata-rata Penyewaan Sepeda")
ax1.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Musim")
st.pyplot(fig1)

st.subheader("Distribusi Penyewaan Sepeda per Musim")
fig2, ax2 = plt.subplots(figsize=(8,5))
sns.boxplot(x='season_name', y='cnt', data=merged_daily, palette="coolwarm", ax=ax2)
ax2.set_xlabel("Musim")
ax2.set_ylabel("Jumlah Penyewaan Sepeda")
ax2.set_title("Distribusi Penyewaan Sepeda per Musim")
st.pyplot(fig2)

st.subheader("Korelasi Variabel Cuaca dan Penyewaan Sepeda")
# Pastikan kolom agregasi dari hourly ada: temp_hour_avg, hum_hour_avg, windspeed_hour_avg
# Jika kolom tersebut tidak ada, pastikan saat penggabungan data sudah ditambahkan
cols_corr = ['temp_hour_avg', 'hum_hour_avg', 'windspeed_hour_avg', 'cnt']
if set(cols_corr).issubset(merged_daily.columns):
    corr_data = merged_daily[cols_corr].corr()
else:
    st.warning("Kolom agregasi hourly tidak ditemukan di dataset merged_daily_data.csv.")
    corr_data = merged_daily[['temp', 'hum', 'windspeed', 'cnt']].corr()

fig3, ax3 = plt.subplots(figsize=(8,5))
sns.heatmap(corr_data, annot=True, cmap="coolwarm", fmt=".2f", ax=ax3)
ax3.set_title("Korelasi antara Variabel Cuaca dan Penyewaan Sepeda")
st.pyplot(fig3)

# ---- BAGIAN 2: DATA HOURLY ----
@st.cache_data
def load_hour_data():
    hour_df = pd.read_csv("Data/hour.csv")
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    return hour_df

hour_df = load_hour_data()

st.header("2. Perbedaan Pola Penyewaan Hari Kerja vs. Hari Libur")
st.subheader("Pola Penyewaan per Jam")

avg_by_hour_working = hour_df.groupby(['hr', 'workingday'])['cnt'].mean().reset_index()

fig4, ax4 = plt.subplots(figsize=(12,6))
sns.lineplot(x='hr', y='cnt', hue='workingday', data=avg_by_hour_working, marker='o', ax=ax4)
ax4.set_xlabel("Jam dalam Sehari")
ax4.set_ylabel("Rata-rata Penyewaan Sepeda")
ax4.set_title("Pola Penyewaan Sepeda per Jam: Hari Kerja vs. Hari Libur")
# Custom legend agar jelas: 0 = Libur, 1 = Hari Kerja
handles, labels = ax4.get_legend_handles_labels()
labels = ['Libur (0)' if lbl=='0' or lbl=='0.0' else 'Hari Kerja (1)' if lbl=='1' or lbl=='1.0' else lbl for lbl in labels]
ax4.legend(handles=handles, labels=labels, title='Working Day')
st.pyplot(fig4)

st.markdown("""
### Insight Utama:
- **Musim & Cuaca:** Penyewaan sepeda cenderung berbeda berdasarkan musim. Misalnya, musim **Summer** biasanya menunjukkan penyewaan yang lebih tinggi, sedangkan **Winter** mungkin menunjukkan penurunan. Korelasi antara variabel cuaca seperti suhu dan kelembaban juga berpengaruh.
- **Hari Kerja vs. Hari Libur:** Pola penyewaan per jam menunjukkan bahwa hari kerja memiliki dua puncak (pagi dan sore) yang mencerminkan kebutuhan beraktivitas, sedangkan hari libur cenderung memiliki pola yang lebih merata atau berbeda.
""")

st.markdown("Dashboard sederhana ini memberikan gambaran visual terkait faktor-faktor yang mempengaruhi penyewaan sepeda. Silakan eksplorasi lebih lanjut atau tambahkan filter sesuai kebutuhan bisnis Anda.")
