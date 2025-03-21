# Submission


**Penjelasan:**
- **Data/**: Folder berisi file data mentah seperti `day.csv` dan `hour.csv`.
- **Dashboard/**: Folder berisi kode aplikasi Streamlit untuk dashboard interaktif.
- **MWP_Proyek_Analisis_Data.ipynb**: Notebook Jupyter yang berisi proses EDA dan visualisasi.
- **requirements.txt**: File yang mendokumentasikan semua paket Python yang diperlukan.

---

## Persiapan Environment & Instalasi Dependencies

Pastikan kamu telah menginstal **Python 3.7+**. Berikut adalah langkah-langkah untuk menyiapkan lingkungan dan menginstal dependensi yang diperlukan:

1. **Clone atau Download Proyek**  
   Unduh seluruh folder proyek ke komputer kamu.

2. **Buat Virtual Environment (Opsional, namun direkomendasikan)**  
   Menggunakan `venv`:
   ```bash
   python -m venv env
   ```
   **Aktifkan Virtual Environment**
   
   `Windows`:
   ```
   env\Scripts\activate
   ```
   `Linux`:
   ```
   source env/bin/activate
   ```
4. Jika file `requirements.txt` sudah ada, jalankan perintah:
   ```
    pip install -r requirements.txt
   ```
   <i>Catatan </i>: Jika belum ada file `requirements.txt`, kamu bisa membuatnya dengan perintah:
   ```
   pip freeze > requirements.txt
   ```
  **Dependencies yang umumnya diperlukan meliputi:**
  ```
  - pandas
  - matplotlib
  - seaborn
  - streamlit
  ```

## Cara Menjalankan Dashboard
- Buka terminal/command prompt dan masuk ke folder Dashboard (Direktori kalian Menyimpan File) :
```
cd Dashboard 
```
```
streamlit run Dashboard.py
```
<i>Catatan </i>: Jika kalian berada di luar Folder `Dashboard` di `Submission` folder maka :
```
streamlit run Dashboard/Dashboard.py
```
## Cara Menjalankan File IPNYB Jupyter Notebook | Google COLAB
 - Buka terminal/command prompt dan masuk ke direktori proyek.
 - Jalankan perintah berikut untuk membuka Jupyter Notebook:
  ```
 jupyter notebook
  ```
 - Buka file MWP_Proyek_Analisis_Data.ipynb dan jalankan sel-sel secara berurutan.

## Dataset
Dataset yang digunakan dalam proyek ini adalah:

- day.csv: Data penyewaan sepeda per hari.
- hour.csv: Data penyewaan sepeda per jam.
- Hasil penggabungan/transformasi data (all_data.csv).

Kolom Penting:

- dteday: Tanggal (harus diubah ke format datetime).
- season: Indikator musim (1=Spring, 2=Summer, 3=Fall, 4=Winter).
- workingday: Indikator hari kerja (0=Libur, 1=Hari Kerja).
- temp, hum, windspeed: Variabel cuaca.
- cnt: Jumlah penyewaan total.
- casual, registered: Jumlah penyewaan berdasarkan segmen pengguna.
