import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set the title of the dashboard
st.title("Proyek Analisis Data Penyewaan Sepeda")

# Load datasets
day_df = pd.read_csv("cd../data/day.csv")
hour_df = pd.read_csv("cd../data/hour.csv")
main_data = pd.read_csv("main_data.csv")

# Convert date columns to datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Jika main_data memiliki kolom 'dteday', pastikan konversi datetime dilakukan
if 'dteday' in main_data.columns:
    main_data['dteday'] = pd.to_datetime(main_data['dteday'])

# Sidebar for user input
st.sidebar.header("Pertanyaan Bisnis")
st.sidebar.subheader("Analisis")
selected_question = st.sidebar.selectbox("Pilih Pertanyaan untuk Analisis", [
    "Pengaruh Kecepatan Angin",
    "Distribusi Penggunaan Sepeda",
    "Pengurangan Penyewaan pada Cuaca Buruk"
])

# Date range input
st.sidebar.subheader("Pilih Rentang Tanggal")
start_date = st.sidebar.date_input("Tanggal Awal", value=day_df['dteday'].min())
end_date = st.sidebar.date_input("Tanggal Akhir", value=day_df['dteday'].max())

# Filter data based on selected date range
filtered_hour_df = hour_df[(hour_df['dteday'] >= pd.to_datetime(start_date)) & (hour_df['dteday'] <= pd.to_datetime(end_date))]
filtered_main_data = main_data[(main_data['dteday'] >= pd.to_datetime(start_date)) & (main_data['dteday'] <= pd.to_datetime(end_date))]

# Function for visualizing windspeed effect
def plot_windspeed_effect():
    X = filtered_hour_df['windspeed']
    y = filtered_hour_df['cnt']
    
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=X, y=y, alpha=0.5)
    plt.title('Pengaruh Kecepatan Angin terhadap Jumlah Penyewaan Sepeda', fontsize=16)
    plt.xlabel('Kecepatan Angin', fontsize=14)
    plt.ylabel('Jumlah Penyewaan', fontsize=14)
    sns.regplot(x=X, y=y, scatter=False, color='orange')
    st.pyplot(plt)

# Function for visualizing usage distribution
def plot_usage_distribution():
    usage_summary = filtered_main_data.groupby(['holiday_hour'])[['casual_hour', 'registered_hour']].mean().reset_index()
    usage_summary['holiday_hour'] = usage_summary['holiday_hour'].map({0: 'Hari Kerja', 1: 'Hari Libur'})

    plt.figure(figsize=(12, 6))
    bar_width = 0.35
    index = range(len(usage_summary))
    
    plt.bar(index, usage_summary['casual_hour'], bar_width, label='Casual', color='skyblue')
    plt.bar([i + bar_width for i in index], usage_summary['registered_hour'], bar_width, label='Registered', color='salmon')
    
    plt.title('Rata-rata Penyewaan Sepeda oleh Pengguna Casual dan Terdaftar', fontsize=16)
    plt.xlabel('Jenis Hari', fontsize=14)
    plt.ylabel('Rata-rata Jumlah Penyewaan', fontsize=14)
    plt.xticks([r + bar_width / 2 for r in index], usage_summary['holiday_hour'])
    plt.legend(title='Tipe Pengguna')
    st.pyplot(plt)

# Function for visualizing weather effect
def plot_weather_effect():
    good_weather = filtered_hour_df[filtered_hour_df['weathersit'].isin([1, 2])]
    bad_weather = filtered_hour_df[filtered_hour_df['weathersit'].isin([3, 4])]
    
    good_weather_avg = good_weather['cnt'].mean()
    bad_weather_avg = bad_weather['cnt'].mean()

    plt.figure(figsize=(12, 6))
    sns.barplot(x=['Cuaca Baik', 'Cuaca Buruk'], y=[good_weather_avg, bad_weather_avg])
    plt.title('Rata-rata Jumlah Penyewaan Sepeda: Cuaca Baik vs Buruk', fontsize=16)
    plt.ylabel('Rata-rata Jumlah Penyewaan', fontsize=14)
    st.pyplot(plt)

# Display the selected question's visualization
if selected_question == "Pengaruh Kecepatan Angin":
    plot_windspeed_effect()
elif selected_question == "Distribusi Penggunaan Sepeda":
    plot_usage_distribution()
elif selected_question == "Pengurangan Penyewaan pada Cuaca Buruk":
    plot_weather_effect()

# Show a brief summary of insights
st.sidebar.subheader("Insights")
if selected_question == "Pengaruh Kecepatan Angin":
    st.sidebar.write("Kecepatan angin memiliki pengaruh negatif terhadap jumlah penyewaan sepeda.")
elif selected_question == "Distribusi Penggunaan Sepeda":
    st.sidebar.write("Pengguna casual cenderung lebih aktif pada hari libur, sementara pengguna terdaftar lebih banyak menggunakan sepeda pada hari kerja.")
elif selected_question == "Pengurangan Penyewaan pada Cuaca Buruk":
    st.sidebar.write("Cuaca buruk mengurangi jumlah penyewaan sepeda secara signifikan.")

# Footer
st.sidebar.text("Dibuat oleh Rafael Aryapati Soebagijo")
