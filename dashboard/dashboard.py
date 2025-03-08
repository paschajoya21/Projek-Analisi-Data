import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import streamlit as st
sns.set(style='dark')

@st.cache_data
def load_data():
    day_df = pd.read_csv("dashboard/day_data.csv", parse_dates=["dteday"])
    return day_df

day_df = load_data()
hour_df = pd.read_csv("dashboard/hour_data.csv")

st.title("Dashboard Peminjaman Sepeda 🚴‍♂️")

st.sidebar.image("logo.png")
st.sidebar.title("Rental Sepeda")
st.sidebar.write("\n")
st.sidebar.write("Dashboard ini menampilkan analisis data peminjaman sepeda berdasarkan berbagai faktor seperti waktu, cuaca, musim, dan jenis pengguna.")
st.sidebar.write("\n") 
st.sidebar.subheader("Pertanyaan Bisnis:")
st.sidebar.write("""
1. Bagaimana perkembangan jumlah peminjamanan dalam perbulan?
2. Apakah di waktu-waktu tertentu terdapat kenaikan jumlah peminjaman sepeda?
3. Apakah musim dan cuaca memperngaruhi jumlah peminjaman sepeda?
4. Bagaimana status user yang meminjam sepedah?
5. Bagaimana jumlah peminjaman di hari libur dan di hari kerja?
""") 
st.sidebar.subheader("Kesimpulan Analisis Berdasarkan Pertanyaan Bisnis:")
st.sidebar.write("""
                 1. Perkembangan dalam 2 tahun terakhir secara keseluruhan memiliki kenaikan di tiap bulan nya, tapi mendapatkan penurunan pada bulan-bulan di akhir tahun
                 2. Terdapatkenaikan yg cukup besar di pagi hari dan sore hari terkusus di jam 8 pagi dan jam 5 sore
                 3. Cuaca sangat mempengaruhi jumlah peminjaman terlihat ketika hujan jumlah peminjaman sangat sedikit, untuk musim cukup mempengaruhi jumlah peminjaman tapi tidak begitu signifikan
                 4. Jumlah user yang meminjam lebih di dominasi oleh peminjam yang telah melakukan registrasi 80'%' lebih banyak di bandingkan peminjam yg belum registrasi (casual user) 
                 5. Peminjaman sepeda lebih banyak dipinjam di hari kerja dibandingkan hari libur
""") 


st.subheader("Jumlah Peminjaman Sepeda Per Bulan")

monthly_df = day_df.resample(rule='ME', on='dteday').agg({
    "yr": "first",
    "cnt": "sum"
})

monthly_df["month"] = monthly_df.index.strftime('%B')
monthly_df = monthly_df.reset_index()
monthly_df.rename(columns={"cnt": "total rentals"}, inplace=True)

years = sorted(monthly_df["yr"].unique())[-2:]

fig, ax = plt.subplots(figsize=(12, 5))
for year in years:
    data_year = monthly_df[monthly_df["yr"] == year]
    ax.plot(data_year["month"], data_year["total rentals"], marker='o', linewidth=2, label=f"Tahun {year}")

ax.set_title("Number of Rentals per Month", fontsize=14)
ax.set_xlabel("Month")
ax.set_ylabel("Total Rentals")
ax.legend()
ax.grid()
st.pyplot(fig)

st.subheader("Pola Peminjaman Sepeda Berdasarkan Waktu")

hourly_rentals = hour_df.groupby("hr")["cnt"].mean()
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=hourly_rentals.index, y=hourly_rentals.values, ax=ax)
ax.set_xlabel("hour")
ax.set_ylabel("Average Rentals")       
ax.set_title("Average Bike Rental per Hour")
ax.set_xticks(range(0, 24))
st.pyplot(fig)

time_rentals = hour_df.groupby(by ="hr_group")["cnt"].sum()
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=time_rentals.index, y=time_rentals.values, ax=ax)
ax.set_xlabel("Time Group")
ax.set_ylabel("Total Rentals")       
ax.set_title("Time Group Rentals")
st.pyplot(fig)

st.subheader("Pengaruh Musim dan Cuaca terhadap Peminjaman Sepeda")

col1, col2 = st.columns(2)
with col1:
    season_rentals = day_df.groupby("season")["cnt"].mean()
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=season_rentals.index, y=season_rentals.values, ax=ax)
    ax.set_xlabel("Season")
    ax.set_ylabel("Average Rentals")
    ax.set_title("Effect of Season on Bike Lending")
    ax.grid()
    st.pyplot(fig)

with col2:
    weather_rentals = hour_df.groupby("weathersit")["cnt"].mean()
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=weather_rentals.index, y=weather_rentals.values, ax=ax)
    ax.set_xlabel("Weather")
    ax.set_ylabel("Average Rentals")
    ax.set_title("Weather Effects on Bike Lending")
    ax.grid()
    st.pyplot(fig)

st.subheader("Distribusi Pengguna Casual vs Registered")
casual_registered = day_df[["casual", "registered"]].sum()
fig, ax = plt.subplots(figsize=(6, 6))
ax.pie(casual_registered, labels=["Casual", "Registered"], autopct='%1.1f%%', colors=["orange", "lightblue"], startangle=90)
ax.set_title("Distribution of Casual vs Registered Users")
st.pyplot(fig)

st.subheader("Perbandingan Peminjaman di Hari Kerja vs Hari Libur")

conditions = [
    (day_df['holiday'] == 'no') & (day_df['workingday'] == 'no'),
    (day_df['holiday'] == 'yes') & (day_df['workingday'] == 'no')
]
values = ['weekend', 'holiday']
day_df['day_category'] = np.select(conditions, values, default='weekday')
category_days_rentals = day_df.groupby(by = "day_category")["cnt"].sum()

fig, ax = plt.subplots(figsize=(6, 5))
sns.barplot(x=category_days_rentals.index, y=category_days_rentals.values, ax=ax)
ax.set_xlabel("Day")
ax.set_ylabel("Total Rentals")
ax.set_title("Weekday vs Holiday Rental Comparison")
ax.grid()   
st.pyplot(fig)
st.caption('Copyright (c) Coding Camp 2025')
