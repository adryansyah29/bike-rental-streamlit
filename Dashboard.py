import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

sewasepedajam_df=pd.read_csv("https://raw.githubusercontent.com/adryansyah29/bike-rental-streamlit/main/all_data.csv")
sewasepedajam_df.head()

# Menyiapkan daily_rent_df
def buat_hari_sewa_df(df):
    hari_sewa_df = df.groupby(by='dteday').agg({
        'cnt': 'sum'
    }).reset_index()
    return hari_sewa_df

# Menyiapkan daily_casual_rent_df
def buat_biasa_sewa_df(df):
    hari_biasa_sewa_df = df.groupby(by='dteday').agg({
        'casual': 'sum'
    }).reset_index()
    return hari_biasa_sewa_df

# Menyiapkan daily_registered_rent_df
def buat_hari_daftar_sewa_df(df):
    hari_daftar_sewa_df = df.groupby(by='dteday').agg({
        'registered': 'sum'
    }).reset_index()
    return hari_daftar_sewa_df
    
# Menyiapkan season_rent_df
def buat_musim_sewa_df(df):
    musim_sewa_df = df.groupby(by='season')[['registered', 'casual']].sum().reset_index()
    return musim_sewa_df

# Menyiapkan monthly_rent_df
def buat_bulanan_sewa_df(df):
    bulanan_sewa_df = df.groupby(by='mnth').agg({
        'cnt': 'sum'})
 
    
    
    return bulanan_sewa_df

# Menyiapkan weekday_rent_df
def buat_mingguan_sewa_df(df):
    mingguan_sewa_df = df.groupby(by='weekday').agg({
        'cnt': 'sum'
    }).reset_index()
    return mingguan_sewa_df

# Menyiapkan workingday_rent_df
def buat_harkerja_sewa_df(df):
    harkerja_sewa_df = df.groupby(by='workingday').agg({
        'cnt': 'sum'
    }).reset_index()
    return harkerja_sewa_df

# Menyiapkan holiday_rent_df
def buat_liburan_sewa_df(df):
    liburan_sewa_df = df.groupby(by='holiday').agg({
        'cnt': 'sum'
    }).reset_index()
    return liburan_sewa_df

# Menyiapkan weather_rent_df
def buat_cuaca_sewa_df(df):
    cuaca_sewa_df = df.groupby(by='weathersit').agg({
        'cnt': 'sum'
    })
    return cuaca_sewa_df

# Membuat komponen filter
min_date = pd.to_datetime(sewasepedajam_df['dteday']).dt.date.min()
max_date = pd.to_datetime(sewasepedajam_df['dteday']).dt.date.max()

with st.sidebar:

    st.image("https://raw.githubusercontent.com/adryansyah29/bike-rental-streamlit/main/sewa_sepedalogo.png")

   # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value= min_date,
        max_value= max_date,
        value=[min_date, max_date]
    )
    main_df = sewasepedajam_df[(sewasepedajam_df['dteday'] >= str(start_date)) & 
                (sewasepedajam_df['dteday'] <= str(end_date))]

    hari_sewa_df = buat_hari_sewa_df(main_df)
    hari_biasa_sewa_df = buat_biasa_sewa_df(main_df)
    hari_daftar_sewa_df = buat_hari_daftar_sewa_df(main_df)
    musim_sewa_df = buat_musim_sewa_df(main_df)
    bulanan_sewa_df = buat_bulanan_sewa_df(main_df)
    mingguan_sewa_df = buat_mingguan_sewa_df(main_df)
    harikerja_sewa_df = buat_harkerja_sewa_df(main_df)
    liburan_sewa_df = buat_liburan_sewa_df(main_df)
    cuaca_sewa_df = buat_cuaca_sewa_df(main_df)

    # Membuat Dashboard secara lengkap

# Membuat judul
st.header('Sewa Sepeda Dashboard')

# Membuat jumlah penyewaan harian
st.subheader('Sewa Harian')
col1, col2, col3 = st.columns(3)

with col1:
    hari_sewa_biasa = hari_biasa_sewa_df['casual'].sum()
    st.metric('Pengguna Biasa', value= hari_sewa_biasa)

with col2:
    hari_sewa_daftar = hari_daftar_sewa_df['registered'].sum()
    st.metric('Pengguna Terdaftar', value= hari_sewa_daftar)
 
with col3:
    hari_sewa_total = hari_sewa_df['cnt'].sum()
    st.metric('Total Pengguna', value= hari_sewa_total)

# Membuat jumlah penyewaan bulanan
st.subheader('Penyewa Dalam Bulanan')
fig, ax = plt.subplots(figsize=(24, 8))
ax.plot(
    bulanan_sewa_df.index,
    bulanan_sewa_df['cnt'],
    marker='o', 
    linewidth=2,
    color='#90CAF9'
)


ax.tick_params(axis='x', labelsize=25, rotation=45)
ax.tick_params(axis='y', labelsize=20)
st.pyplot(fig)

# Membuat jumlah penyewaan berdasarkan season
st.subheader('Penyewa pada musim')

fig, ax = plt.subplots(figsize=(16, 8))

sns.barplot(
    x='season',
    y='registered',
    data=musim_sewa_df,
    label='Registered',
    color='tab:blue',
    ax=ax
)

sns.barplot(
    x='season',
    y='casual',
    data=musim_sewa_df,
    label='Casual',
    color='tab:orange',
    ax=ax
)

for index, row in musim_sewa_df.iterrows():
    ax.text(index, row['registered'], str(row['registered']), ha='center', va='bottom', fontsize=12)
    ax.text(index, row['casual'], str(row['casual']), ha='center', va='bottom', fontsize=12)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20, rotation=0)
ax.tick_params(axis='y', labelsize=15)
ax.legend()
st.pyplot(fig)

# Membuah jumlah penyewaan berdasarkan kondisi cuaca
st.subheader('Penyewa pada cuaca')

fig, ax = plt.subplots(figsize=(16, 8))

colors=["tab:blue", "tab:orange", "tab:green"]

sns.barplot(
    x=cuaca_sewa_df.index,
    y=cuaca_sewa_df['cnt'],
    palette=colors,
    ax=ax
)

for index, row in enumerate(cuaca_sewa_df['cnt']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)

# Membuat jumlah penyewaan berdasarkan weekday, working dan holiday
st.subheader('Penyewa Pada Hari Biasa,Hari libur ,dan Hari Minggu')

fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(15,10))

colors1=["tab:blue", "tab:orange"]
colors2=["tab:blue", "tab:orange"]
colors3=["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple", "tab:brown", "tab:pink"]

# Berdasarkan workingday
sns.barplot(
    x='workingday',
    y='cnt',
    data=harikerja_sewa_df,
    palette=colors1,
    ax=axes[0])

for index, row in enumerate(harikerja_sewa_df['cnt']):
    axes[0].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

axes[0].set_title('Jumlah penyewa pada hari kerja')
axes[0].set_ylabel(None)
axes[0].tick_params(axis='x', labelsize=15)
axes[0].tick_params(axis='y', labelsize=10)

# Berdasarkan holiday
sns.barplot(
  x='holiday',
  y='cnt',
  data=liburan_sewa_df,
  palette=colors2,
  ax=axes[1])

for index, row in enumerate(liburan_sewa_df['cnt']):
    axes[1].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

axes[1].set_title('Jumlah penyewa pada hari libur')
axes[1].set_ylabel(None)
axes[1].tick_params(axis='x', labelsize=15)
axes[1].tick_params(axis='y', labelsize=10)

# Berdasarkan weekday
sns.barplot(
  x='weekday',
  y='cnt',
  data=mingguan_sewa_df,
  palette=colors3,
  ax=axes[2])

for index, row in enumerate(mingguan_sewa_df['cnt']):
    axes[2].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

axes[2].set_title('penyewa sepeda pada mingguan')
axes[2].set_ylabel(None)
axes[2].tick_params(axis='x', labelsize=15)
axes[2].tick_params(axis='y', labelsize=10)

plt.tight_layout()
st.pyplot(fig)
st.caption('Copyright (c) Aditya Ryan 2024')
