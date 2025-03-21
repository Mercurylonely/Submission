import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Konfigurasi tampilan grafik
sns.set(style="whitegrid")
plt.rcParams.update({'figure.max_open_warning': 0})

st.title("Dashboard Analisis Penyewaan Sepeda Interaktif")

st.markdown("""
Dashboard ini menyajikan insight mengenai:
- **Pengaruh Cuaca dan Musim** terhadap jumlah penyewaan sepeda.
- **Perbedaan Pola Penyewaan** antara hari kerja dan hari libur, terutama pada jam-jam tertentu.

Gunakan filter di sidebar untuk melakukan eksplorasi data secara interaktif.
""")

# ========= SIDEBAR FILTER DATA HARIAN =========
st.sidebar.header("Filter Data Harian")
@st.cache_data
def load_merged_daily_data():
    # Pastikan path file sudah sesuai, misalnya "Dashboard/all_data.csv"
    merged_daily = pd.read_csv("Dashboard/all_data.csv")
    merged_daily['dteday'] = pd.to_datetime(merged_daily['dteday'])
    # Buat kolom season_name berdasarkan kolom 'season'
    season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    merged_daily['season_name'] = merged_daily['season'].map(season_mapping)
    return merged_daily

merged_daily = load_merged_daily_data()

# Filter tanggal berdasarkan data harian
min_date = merged_daily['dteday'].min()
max_date = merged_daily['dteday'].max()
date_range = st.sidebar.date_input("Pilih rentang tanggal", [min_date, max_date],
                                    min_value=min_date, max_value=max_date)

# Filter musim
selected_seasons = st.sidebar.multiselect("Pilih musim", 
                                            options=['Spring','Summer','Fall','Winter'], 
                                            default=['Spring','Summer','Fall','Winter'])

# Filter data harian berdasarkan input sidebar
filtered_daily = merged_daily[
    (merged_daily['dteday'] >= pd.to_datetime(date_range[0])) &
    (merged_daily['dteday'] <= pd.to_datetime(date_range[1])) &
    (merged_daily['season_name'].isin(selected_seasons))
]

# ========= BAGIAN 1: ANALISIS DATA HARIAN =========
st.header("1. Pengaruh Cuaca dan Musim")
st.subheader("Rata-rata Penyewaan Sepeda per Musim")

if filtered_daily.empty:
    st.warning("Tidak ada data untuk kriteria yang dipilih. Silakan ubah filter.")
else:
    avg_season = filtered_daily.groupby('season_name')['cnt'].mean().reindex(['Spring','Summer','Fall','Winter'])
    
    fig1, ax1 = plt.subplots(figsize=(8,5))
    sns.barplot(x=avg_season.index, y=avg_season.values, palette="coolwarm", ax=ax1)
    ax1.set_xlabel("Musim")
    ax1.set_ylabel("Rata-rata Penyewaan Sepeda")
    ax1.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Musim")
    st.pyplot(fig1)
    
    st.subheader("Distribusi Penyewaan Sepeda per Musim")
    fig2, ax2 = plt.subplots(figsize=(8,5))
    sns.boxplot(x='season_name', y='cnt', data=filtered_daily, palette="coolwarm", ax=ax2)
    ax2.set_xlabel("Musim")
    ax2.set_ylabel("Jumlah Penyewaan Sepeda")
    ax2.set_title("Distribusi Penyewaan Sepeda per Musim")
    st.pyplot(fig2)
    
    st.subheader("Korelasi Variabel Cuaca dan Penyewaan Sepeda")
    # Gunakan kolom agregasi hourly jika ada, jika tidak gunakan kolom aslinya
    cols_corr = ['temp_hour_avg', 'hum_hour_avg', 'windspeed_hour_avg', 'cnt']
    if set(cols_corr).issubset(filtered_daily.columns):
        corr_data = filtered_daily[cols_corr].corr()
    else:
        corr_data = filtered_daily[['temp', 'hum', 'windspeed', 'cnt']].corr()
    
    fig3, ax3 = plt.subplots(figsize=(8,5))
    sns.heatmap(corr_data, annot=True, cmap="coolwarm", fmt=".2f", ax=ax3)
    ax3.set_title("Korelasi antara Variabel Cuaca dan Penyewaan Sepeda")
    st.pyplot(fig3)
    
    # Insight untuk Data Harian
    st.markdown("#### Insight - Pengaruh Cuaca dan Musim")
    st.markdown("""
    - **Insight:**  
      Penyewaan sepeda cenderung lebih tinggi di musim *Fall* dan menurun di musim *Winter*. Korelasi positif antara suhu dan jumlah penyewaan menunjukkan bahwa cuaca hangat mendukung peningkatan penyewaan.
    
    - **Rekomendasi:**  
      1. **Penambahan Jumlah Unit Sepeda:**  
         Meningkatkan jumlah sepeda pada musim panas untuk mengakomodasi permintaan yang tinggi.
      2. **Promosi Musiman:**  
         Mengadakan promosi atau diskon di musim dingin untuk menarik lebih banyak penyewa, terutama pengguna casual.
      3. **Optimasi Operasional:**  
         Menggunakan data korelasi untuk memprediksi permintaan berdasarkan cuaca sehingga dapat mengatur pengadaan Unit secara lebih efisien.
    """)
    
# ========= SIDEBAR FILTER DATA HOURLY =========
st.sidebar.header("Filter Data Per Jam")
@st.cache_data
def load_hour_data():
    hour_df = pd.read_csv("Data/hour.csv")
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    return hour_df

hour_df = load_hour_data()

# Filter untuk kategori hari kerja
workingday_option = st.sidebar.radio("Pilih Hari:", options=["Semua", "Hari Kerja", "Libur"])
if workingday_option == "Hari Kerja":
    filtered_hour = hour_df[hour_df['workingday'] == 1]
elif workingday_option == "Libur":
    filtered_hour = hour_df[hour_df['workingday'] == 0]
else:
    filtered_hour = hour_df.copy()

# Filter rentang jam
min_hr = int(filtered_hour['hr'].min())
max_hr = int(filtered_hour['hr'].max())
hr_range = st.sidebar.slider("Pilih rentang jam", min_value=min_hr, max_value=max_hr, value=(min_hr, max_hr))

filtered_hour = filtered_hour[(filtered_hour['hr'] >= hr_range[0]) & (filtered_hour['hr'] <= hr_range[1])]

# ========= BAGIAN 2: ANALISIS DATA HOURLY =========
st.header("2. Perbedaan Pola Penyewaan Hari Kerja vs. Hari Libur")
st.subheader("Pola Penyewaan per Jam ")

if filtered_hour.empty:
    st.warning("Tidak ada data per jam untuk kriteria yang dipilih. Silakan ubah filter.")
else:
    avg_by_hour_working = filtered_hour.groupby(['hr', 'workingday'])['cnt'].mean().reset_index()
    
    fig4, ax4 = plt.subplots(figsize=(12,6))
    sns.lineplot(x='hr', y='cnt', hue='workingday', data=avg_by_hour_working, marker='o', ax=ax4)
    ax4.set_xlabel("Jam dalam Sehari")
    ax4.set_ylabel("Rata-rata Penyewaan Sepeda")
    ax4.set_title("Pola Penyewaan Sepeda per Jam: Hari Kerja vs. Hari Libur")
    # Kustomisasi legend untuk lebih jelas: 0 = Libur, 1 = Hari Kerja
    handles, labels = ax4.get_legend_handles_labels()
    labels = ['Libur (0)' if lbl in ['0', '0.0'] else 'Hari Kerja (1)' if lbl in ['1', '1.0'] else lbl for lbl in labels]
    ax4.legend(handles=handles, labels=labels, title='Working Day')
    st.pyplot(fig4)
    
    # Insight & Rekomendasi untuk Data Per Jam
    st.markdown("#### Insight  - Pola Penyewaan per Jam")
    st.markdown("""
    - **Insight:**  
      Pola penyewaan menunjukkan dua puncak utama pada hari kerja, yaitu pada pagi dan sore hari, yang mencerminkan aktivitas Sedang Padat Sekali. Pada hari libur, pola penyewaan lebih merata dan tidak menunjukkan puncak yang tajam.
    
    - **Rekomendasi:**  
      1. **Pengaturan Unit:**  
         Memastikan adanya ketersediaan sepeda lebih banyak pada jam-jam puncak hari kerja.
      2. **Strategi Pemasaran:**  
         Menyesuaikan promosi untuk meningkatkan penyewaan di luar jam yang menjadi insight paling tinggi (puncak) atau pada hari libur.
      3. **Penjadwalan Pemeliharaan:**  
         Menjadwalkan pemeliharaan sepeda pada jam-jam dengan penyewaan rendah untuk meminimalisir gangguan operasional yang akan membuat penyewa merasa tidak nyaman sehingga akan menurunkan Penyewaan pada jam-jam tersebut.
    """)
