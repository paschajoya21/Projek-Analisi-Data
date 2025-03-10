import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import streamlit as st
import datetime
sns.set(style='dark')

st.title("Dashboard Peminjaman Sepeda 🚴‍♂️")

st.sidebar.image("dashboard/logo.png")
st.sidebar.title("Rental Sepeda")
st.sidebar.write("\n")
st.sidebar.write("Dashboard ini menampilkan analisis data peminjaman sepeda berdasarkan berbagai faktor seperti waktu, cuaca, musim, dan jenis pengguna.")
st.sidebar.write("\n") 
st.sidebar.subheader("Pertanyaan Bisnis:")
st.sidebar.write("""
1. Bagaimana perkembangan jumlah peminjamanan dalam perbulan?
2. Bagaimana tren jumlah peminjaman sepeda berdasarkan waktu tertentu dan kapan terjadi lonjakan peminjaman tertinggi?
3. Sejauh mana musim dan kondisi cuaca mempengaruhi jumlah peminjaman sepeda, dan faktor cuaca apa yang memiliki dampak paling besar?
4. Bagaimana status user yang meminjam sepedah?
5. Bagaimana jumlah peminjaman di hari libur dan di hari kerja?
""") 
st.sidebar.subheader("Kesimpulan Analisis Berdasarkan Pertanyaan Bisnis:")
st.sidebar.write("""
                 1. Berdasarkan data dua tahun terakhir, jumlah peminjaman sepeda secara keseluruhan mengalami tren peningkatan setiap bulan. Pada tahun pertama terdapat kenaikan yang cukup signifikan dari milai bulan Februari hingga Mei dan di bulan bulan setelah nya cukup stagnan dan mendapat penurunan dengan skala yang kecil hingga di bulan Oktober terjadi penurunan yg cukup besar hingga akhir tahun. Sedangkan di tahun kedua terjadi kenaikan yg sangan signifikan terjadi di bulan Februari, kenaikan terus berjalan secara perlahan hingga mendekati akhir tahun mengalami penurunan kembali seperti pada tahun pertama. Penurunan ini kemungkinan disebabkan oleh faktor cuaca, musim dan juga perubahan pola aktivitas pengguna, seperti libur akhir tahun. 
                 2. Analisis terhadap pola waktu menunjukkan lonjakan peminjaman terbesar terjadi pada pukul 08.00 pagi dan 17.00 sore, dan pada siang hari tidak ada penurunan yang terlalu drastis. Hal ini menunjukan bahwa kemungkinan sepeda banyak digunakan sebagai sarana transportasi harian khusunya seperti untuk berangkat dan pulang kerja atau sekolah.
                 3. Cuaca memiliki dampak yang signifikan terhadap jumlah peminjaman sepeda. Saat cerah, jumlah penminjaman sepedah mengalami kenaikan sangat drastis. Sedangkan saat hujan, jumlah peminjaman mengalami penurunan drastis. Sementara itu, perubahan musim memiliki pengaruh yang lebih kecil terhadap jumlah peminjaman dibandingkan cuaca harian.
                 4. Sebagian besar pengguna yang meminjam sepeda adalah pengguna yang sudah registrasi, yang jumlahnya mencapai lebih dari 80'%' lebih banyak dibandingkan pengguna biasa (casual users). Ini menunjukkan bahwa pengguna yang sudah registrasi lebih sering menggunakan layanan dan menadikan sepedah alat transportasi harian mereka dibandingkan pengguna yang tidak terdaftar.
                 5. Aktivitas peminjaman lebih tinggi pada hari kerja dibandingkan hari libur. Hal ini mendukung pembahasan sebelumnya bahwa sepeda sering digunakan untuk transportasi harian, bukan sekadar rekreasi.
""")


@st.cache_data
def load_data():
    day_df = pd.read_csv("dashboard/day_data.csv", parse_dates=["dteday"])
    hour_df = pd.read_csv("dashboard/hour_data.csv",  parse_dates=["dteday"])
    return day_df, hour_df

day_df, hour_df = load_data()

selectionTime = st.selectbox(
    label="Pilihan Rentan Waktu:",
    options=('Pertahun', 'Perbulan', 'Perhari')
)
if selectionTime == "Perbulan":
    col1, col2 = st.columns(2)
    with col1:
        selectionMnth = st.selectbox(
            label="Pilihan Bulan:",
            options=('Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 
                    'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember')
        )
    with col2:
        selectionYr = st.selectbox("Pilih Tahun:", sorted(day_df["dteday"].dt.year.unique()))

elif selectionTime == "Perhari":
    selectionDate = st.date_input(
        label='Pilih Tanggal', 
        min_value=datetime.date(2011, 1, 1), 
        max_value=datetime.date(2012, 12, 31)
    )


st.subheader("Jumlah Peminjaman Sepeda")



fig, ax = plt.subplots(figsize=(12, 5))

if selectionTime == "Pertahun":
    monthly_df = day_df.resample(rule='ME', on='dteday').agg({ 
        "yr": "first",
        "cnt": "sum"
    })
    monthly_df["month"] = monthly_df.index.strftime('%B')
    monthly_df = monthly_df.reset_index()
    monthly_df.rename(columns={"cnt": "total_rentals"}, inplace=True)

    years = sorted(monthly_df["yr"].unique())[-2:]

    for year in years:
        data_year = monthly_df[monthly_df["yr"] == year]
        ax.plot(data_year["month"], data_year["total_rentals"], marker='o', linewidth=2, label=f"Tahun {year}")

    col1, col2, col3 = st.columns(3)

    with col1:
        MaxCnt = monthly_df.total_rentals.max()
        st.metric("Peminjaman Terbanyak", value= MaxCnt)
    with col2:
        MinCnt = monthly_df.total_rentals.min()
        st.metric("Peminjaman Tersedikit", value= MinCnt)
    with col3:
        AvgCnt = monthly_df.total_rentals.mean()
        st.metric("Rata-rata Pemimjaman", value= AvgCnt)

    ax.set_title("Number of Rentals per Month", fontsize=14)
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Rentals")
    ax.legend()
    ax.grid()

elif selectionTime == "Perbulan":
    month_map = {
        'Januari': 1, 'Februari': 2, 'Maret': 3, 'April': 4, 'Mei': 5, 'Juni': 6, 
        'Juli': 7, 'Agustus': 8, 'September': 9, 'Oktober': 10, 'November': 11, 'Desember': 12
    }

    selected_year = selectionYr
    selected_month = month_map[selectionMnth]
    daily_df = day_df[(day_df["dteday"].dt.month == selected_month) & (day_df["dteday"].dt.year == selected_year) ]

    col1, col2, col3 = st.columns(3)

    with col1:
        MaxCnt = daily_df.cnt.max()
        st.metric("Peminjaman Terbanyak", value= MaxCnt)
    with col2:
        MinCnt = daily_df.cnt.min()
        st.metric("Peminjaman Tersedikit", value= MinCnt)
    with col3:
        AvgCnt = daily_df.cnt.mean()
        st.metric("Rata-rata Pemimjaman", value= AvgCnt)

    sns.lineplot(data=daily_df, x="dteday", y="cnt", marker='o', linewidth=2, ax=ax)
    ax.set_title(f"Daily Rentals in {selectionMnth}", fontsize=14)
    ax.set_xlabel("Date")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    ax.set_ylabel("Total Rentals")
    ax.grid()

elif selectionTime == "Perhari":
    hourly_df_filtered = hour_df[hour_df["dteday"] == pd.to_datetime(selectionDate)]

    col1, col2, col3 = st.columns(3)

    with col1:
        MaxCnt = hourly_df_filtered.cnt.max()
        st.metric("Peminjaman Terbanyak", value= MaxCnt)
    with col2:
        MinCnt = hourly_df_filtered.cnt.min()
        st.metric("Peminjaman Tersedikit", value= MinCnt)
    with col3:
        AvgCnt = hourly_df_filtered.cnt.mean()
        st.metric("Rata-rata Pemimjaman", value= AvgCnt)

    sns.lineplot(data=hourly_df_filtered, x="hr", y="cnt", marker='o', linewidth=2, ax=ax)
    ax.set_title(f"Hourly Rentals on {selectionDate}", fontsize=14)
    ax.set_xlabel("Hour")
    ax.set_ylabel("Total Rentals")
    ax.set_xticks(range(0, 24))
    ax.grid()

st.pyplot(fig)

st.subheader("Pola Peminjaman Sepeda Berdasarkan Waktu")

fig, ax = plt.subplots(figsize=(10, 5))

if selectionTime == "Pertahun":
    hourly_rentals = hour_df.groupby("hr")["cnt"].mean()
    sns.barplot(x=hourly_rentals.index, y=hourly_rentals.values, ax=ax)
    ax.set_title("Average Bike Rental per Hour (Overall)", fontsize=14)

elif selectionTime == "Perbulan":
    hourly_rentals = hour_df[
        (hour_df["dteday"].dt.year == selectionYr) & (hour_df["dteday"].dt.month == selected_month)
    ].groupby("hr")["cnt"].mean()

    sns.barplot(x=hourly_rentals.index, y=hourly_rentals.values, ax=ax)
    ax.set_title(f"Average Bike Rental per Hour in {selectionMnth} {selectionYr}", fontsize=14)

elif selectionTime == "Perhari":
    hourly_rentals = hour_df[hour_df["dteday"] == pd.to_datetime(selectionDate)].groupby("hr")["cnt"].sum()
    
    sns.barplot(x=hourly_rentals.index, y=hourly_rentals.values, ax=ax)
    ax.set_title(f"Bike Rentals per Hour on {selectionDate}", fontsize=14)

ax.set_xlabel("Hour")
ax.set_ylabel("Average Rentals")
ax.set_xticks(range(0, 24))
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(10, 5))

if selectionTime == "Pertahun":
    time_rentals = hour_df.groupby("hr_group")["cnt"].sum()
    ax.set_title("Total Rentals per Time Group (Overall)", fontsize=14)

elif selectionTime == "Perbulan":
    time_rentals = hour_df[
        (hour_df["dteday"].dt.year == selectionYr) & (hour_df["dteday"].dt.month == selected_month)
    ].groupby("hr_group")["cnt"].sum()
    
    ax.set_title(f"Total Rentals per Time Group in {selectionMnth} {selectionYr}", fontsize=14)

elif selectionTime == "Perhari":
    time_rentals = hour_df[hour_df["dteday"] == pd.to_datetime(selectionDate)].groupby("hr_group")["cnt"].sum()
    
    ax.set_title(f"Total Rentals per Time Group on {selectionDate}", fontsize=14)

sns.barplot(x=time_rentals.index, y=time_rentals.values, ax=ax)
ax.set_xlabel("Time Group")
ax.set_ylabel("Total Rentals")
st.pyplot(fig)

st.subheader("Pengaruh Musim dan Cuaca terhadap Peminjaman Sepeda")

col1, col2 = st.columns(2)
with col1:
    fig, ax = plt.subplots(figsize=(8, 5))
    
    if selectionTime == "Pertahun":
        season_rentals = day_df.groupby("season")["cnt"].sum()
        ax.set_title("Effect of Season on Bike Lending (Overall)", fontsize=14)
    
    elif selectionTime == "Perbulan":
        season_rentals = day_df[
            (day_df["dteday"].dt.year == selectionYr) & (day_df["dteday"].dt.month == selected_month)
        ].groupby("season")["cnt"].sum()
        ax.set_title(f"Effect of Season on Bike Lending in {selectionMnth} {selectionYr}", fontsize=14)

    elif selectionTime == "Perhari":
        season_rentals = day_df[day_df["dteday"] == pd.to_datetime(selectionDate)].groupby("season")["cnt"].sum()
        ax.set_title(f"Effect of Season on {selectionDate}", fontsize=14)

    sns.barplot(x=season_rentals.index, y=season_rentals.values, ax=ax)
    ax.set_xlabel("Season")
    ax.set_ylabel("Total Rentals")
    ax.grid()
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(8, 5))
    
    if selectionTime == "Pertahun":
        weather_rentals = hour_df.groupby("weathersit")["cnt"].sum()
        ax.set_title("Weather Effects on Bike Lending (Overall)", fontsize=14)

    elif selectionTime == "Perbulan":
        weather_rentals = hour_df[
            (hour_df["dteday"].dt.year == selectionYr) & (hour_df["dteday"].dt.month == selected_month)
        ].groupby("weathersit")["cnt"].sum()
        ax.set_title(f"Weather Effects on Bike Lending in {selectionMnth} {selectionYr}", fontsize=14)

    elif selectionTime == "Perhari":
        weather_rentals = hour_df[hour_df["dteday"] == pd.to_datetime(selectionDate)].groupby("weathersit")["cnt"].sum()
        ax.set_title(f"Weather Effects on {selectionDate}", fontsize=14)

    sns.barplot(x=weather_rentals.index, y=weather_rentals.values, ax=ax)
    ax.set_xlabel("Weather")
    ax.set_ylabel("Total Rentals")
    ax.grid()
    st.pyplot(fig)

st.subheader("Distribusi Pengguna Casual vs Registered")

if selectionTime == "Pertahun":
    casual_registered = day_df[["casual", "registered"]].sum()
    title_text = "Distribution of Casual vs Registered Users (Overall)"

elif selectionTime == "Perbulan":
    casual_registered = day_df[
        (day_df["dteday"].dt.year == selectionYr) & (day_df["dteday"].dt.month == selected_month)
    ][["casual", "registered"]].sum()
    title_text = f"Distribution in {selectionMnth} {selectionYr}"

elif selectionTime == "Perhari":
    casual_registered = day_df[day_df["dteday"] == pd.to_datetime(selectionDate)][["casual", "registered"]].sum()
    title_text = f"Distribution on {selectionDate}"

fig, ax = plt.subplots(figsize=(6, 6))
ax.pie(
    casual_registered, labels=["Casual", "Registered"], autopct='%1.1f%%', 
    colors=["orange", "lightblue"], startangle=90
)
ax.set_title(title_text)
st.pyplot(fig)


st.subheader("Perbandingan Peminjaman di Hari Kerja vs Hari Libur")

if selectionTime == "Pertahun":
    filtered_df = day_df
    title_text = "Weekday vs Holiday Rental Comparison (Overall)"

elif selectionTime == "Perbulan":
    filtered_df = day_df[
        (day_df["dteday"].dt.year == selectionYr) & (day_df["dteday"].dt.month == selected_month)
    ]
    title_text = f"Weekday vs Holiday Rental in {selectionMnth} {selectionYr}"

elif selectionTime == "Perhari":
    filtered_df = day_df[day_df["dteday"] == pd.to_datetime(selectionDate)]
    title_text = f"Weekday vs Holiday Rental on {selectionDate}"

conditions = [
    (filtered_df['holiday'] == 'no') & (filtered_df['workingday'] == 'no'),
    (filtered_df['holiday'] == 'yes') & (filtered_df['workingday'] == 'no')
]
values = ['weekend', 'holiday']
filtered_df['day_category'] = np.select(conditions, values, default='weekday')

category_days_rentals = filtered_df.groupby("day_category")["cnt"].sum()

fig, ax = plt.subplots(figsize=(6, 5))
sns.barplot(x=category_days_rentals.index, y=category_days_rentals.values, ax=ax)
ax.set_xlabel("Day Category")
ax.set_ylabel("Total Rentals")
ax.set_title(title_text)
ax.grid()
st.pyplot(fig)

st.caption('Copyright (c) Coding Camp 2025')
