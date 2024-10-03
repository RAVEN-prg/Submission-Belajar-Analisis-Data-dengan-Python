import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
main_data = pd.read_csv("dashboard/main_data.csv")

# Convert the 'dteday' column to datetime if not already
main_data['dteday'] = pd.to_datetime(main_data['dteday'])

# Title of the dashboard
st.title("Dashboard Analisis Penyewaan Sepeda")

# Sidebar
st.sidebar.header("Pengaturan Tampilan")

# Rentang tanggal
min_date = main_data['dteday'].min()
max_date = main_data['dteday'].max()

start_date, end_date = st.sidebar.date_input(
    label='Rentang Waktu', min_value=min_date,
    max_value=max_date, value=[min_date, max_date]
)

# Filter data berdasarkan rentang tanggal
filtered_data = main_data[(main_data['dteday'] >= pd.to_datetime(start_date)) & 
                          (main_data['dteday'] <= pd.to_datetime(end_date))]

# Pilih analisis
analysis_type = st.sidebar.selectbox("Pilih Analisis", ("Pengaruh Cuaca", "Pengaruh Kecepatan Angin", "Penggunaan Casual vs Terdaftar"))

# Helper function to create plot
def plot_wind_speed_vs_cnt():
    st.subheader("Pengaruh Kecepatan Angin terhadap Jumlah Penyewaan Sepeda")
    
    # Scatter plot with regression line
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=filtered_data['windspeed_hour'], y=filtered_data['cnt_hour'], alpha=0.5)
    sns.regplot(x=filtered_data['windspeed_hour'], y=filtered_data['cnt_hour'], scatter=False, color='orange')
    
    plt.title('Pengaruh Kecepatan Angin terhadap Jumlah Penyewaan Sepeda')
    plt.xlabel('Kecepatan Angin (Normalisasi)')
    plt.ylabel('Jumlah Penyewaan')
    plt.grid()
    
    st.pyplot(plt)

def plot_weather_vs_cnt():
    st.subheader("Rata-rata Penyewaan Sepeda: Cuaca Baik vs Cuaca Buruk")

    # Data Cuaca Baik dan Buruk
    good_weather = filtered_data[filtered_data['weathersit_hour'].isin([1, 2])]
    bad_weather = filtered_data[filtered_data['weathersit_hour'].isin([3, 4])]
    
    good_weather_avg = good_weather['cnt_hour'].mean()
    bad_weather_avg = bad_weather['cnt_hour'].mean()
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x=['Cuaca Baik', 'Cuaca Buruk'], y=[good_weather_avg, bad_weather_avg])
    plt.title('Rata-rata Jumlah Penyewaan Sepeda: Cuaca Baik vs Buruk')
    plt.ylabel('Rata-rata Jumlah Penyewaan')
    plt.grid()

    st.pyplot(plt)

def plot_casual_vs_registered():
    st.subheader("Rata-rata Penyewaan Sepeda oleh Pengguna Casual dan Terdaftar")

    usage_summary = filtered_data.groupby(['holiday_hour'])[['casual_hour', 'registered_hour']].mean().reset_index()
    usage_summary['holiday_hour'] = usage_summary['holiday_hour'].map({0: 'Hari Kerja', 1: 'Hari Libur'})

    plt.figure(figsize=(10, 6))
    bar_width = 0.35
    index = range(len(usage_summary))

    plt.bar(index, usage_summary['casual_hour'], bar_width, label='Casual', color='skyblue')
    plt.bar([i + bar_width for i in index], usage_summary['registered_hour'], bar_width, label='Registered', color='salmon')

    for i in index:
        plt.text(i, usage_summary['casual_hour'][i] + 5, f"{usage_summary['casual_hour'][i]:.1f}", ha='center')
        plt.text(i + bar_width, usage_summary['registered_hour'][i] + 5, f"{usage_summary['registered_hour'][i]:.1f}", ha='center')

    plt.title('Rata-rata Penyewaan Sepeda oleh Pengguna Casual dan Terdaftar')
    plt.xticks([r + bar_width / 2 for r in index], usage_summary['holiday_hour'])
    plt.ylabel('Rata-rata Penyewaan')
    plt.legend()

    st.pyplot(plt)

# Display analysis based on user choice
if analysis_type == "Pengaruh Cuaca":
    plot_weather_vs_cnt()
elif analysis_type == "Pengaruh Kecepatan Angin":
    plot_wind_speed_vs_cnt()
elif analysis_type == "Penggunaan Casual vs Terdaftar":
    plot_casual_vs_registered()
