import streamlit as st
import pandas as pd
import plotly.express as px
import gdown

# Unduh dataset dari Google Drive
file_id = '1ScbfBeekkbqOdJupECBv3MtFnffKFXgJ'  # ID file dari URL Google Drive
gdown.download(f'https://drive.google.com/uc?id={file_id}', 'Electric_Vehicle_Population_Data.csv', quiet=False)

# Load dataset
data_path = "Electric_Vehicle_Population_Data.csv"
data = pd.read_csv(data_path)

# Page Title
st.title("Dashboard Populasi Kendaraan Listrik")
st.markdown(
    """
    Dashboard ini menyediakan analisis visual dari data populasi kendaraan listrik.
    Anda dapat menjelajahi berbagai visualisasi untuk memahami tren, distribusi, 
    dan hubungan dalam data kendaraan listrik.
    """
)

# Sidebar Header
st.sidebar.title("Navigasi Dashboard")

# Sidebar untuk memilih visualisasi
visualization_choice = st.sidebar.radio(
    "Pilih Visualisasi:",
    options=[
        "Distribusi Tahun Model Kendaraan",
        "Rata-rata Jarak Tempuh Berdasarkan Jenis Kendaraan",
        "Hubungan antara Harga Dasar dan Jarak Tempuh"
    ]
)

# Visualisasi 1: Distribusi Tahun Model
if visualization_choice == "Distribusi Tahun Model Kendaraan":
    st.header("Distribusi Tahun Model Kendaraan Listrik")
    st.markdown(
        """
        Visualisasi ini menunjukkan distribusi tahun pembuatan kendaraan listrik dalam dataset. 
        Histogram ini membantu kita memahami tren pembuatan kendaraan listrik di berbagai tahun. 
        Apakah ada lonjakan tertentu pada periode tertentu? Anda dapat menggunakan informasi ini 
        untuk melihat bagaimana industri kendaraan listrik telah berkembang dari waktu ke waktu.
        """
    )
    fig_year = px.histogram(
        data,
        x="Model Year",
        nbins=20,
        title="Distribusi Tahun Model Kendaraan Listrik",
        labels={"Model Year": "Tahun Model"},
        color_discrete_sequence=["#636EFA"]
    )
    st.plotly_chart(fig_year)

# Visualisasi 2: Jenis Kendaraan dan Jangkauan Listrik
elif visualization_choice == "Rata-rata Jarak Tempuh Berdasarkan Jenis Kendaraan":
    st.header("Rata-rata Jarak Tempuh Berdasarkan Jenis Kendaraan")
    st.markdown(
        """
        Visualisasi ini menampilkan rata-rata jarak tempuh listrik berdasarkan jenis kendaraan.
        Setiap jenis kendaraan memiliki kemampuan jangkauan yang berbeda. 
        Bar chart ini membantu kita mengidentifikasi jenis kendaraan mana yang memiliki 
        jarak tempuh rata-rata lebih tinggi, yang berguna untuk analisis pasar dan preferensi konsumen.
        """
    )
    avg_range = data.groupby("Electric Vehicle Type")["Electric Range"].mean().reset_index()
    fig_range = px.bar(
        avg_range,
        x="Electric Vehicle Type",
        y="Electric Range",
        title="Rata-rata Jarak Tempuh Berdasarkan Jenis Kendaraan",
        labels={"Electric Vehicle Type": "Jenis Kendaraan", "Electric Range": "Jarak Tempuh (Mil)"},
        color="Electric Range",
        color_continuous_scale="Viridis"
    )
    st.plotly_chart(fig_range)

# Visualisasi 3: Hubungan antara Harga Dasar dan Jarak Tempuh
elif visualization_choice == "Hubungan antara Harga Dasar dan Jarak Tempuh":
    st.header("Hubungan antara Harga Dasar dan Jarak Tempuh")
    st.markdown(
        """
        Scatter plot ini menunjukkan hubungan antara harga dasar kendaraan (Base MSRP) 
        dan jarak tempuh listriknya (Electric Range). Visualisasi ini membantu kita 
        melihat apakah kendaraan dengan harga lebih tinggi cenderung memiliki 
        jarak tempuh listrik yang lebih baik. Analisis ini berguna dalam memahami 
        trade-off antara biaya dan performa kendaraan listrik.
        """
    )
    if "Base MSRP" in data.columns and "Electric Range" in data.columns:
        fig_scatter = px.scatter(
            data,
            x="Base MSRP",
            y="Electric Range",
            color="Make",
            size="Electric Range",
            hover_data=["Model", "Electric Vehicle Type"],
            title="Hubungan antara Harga Dasar dan Jarak Tempuh",
            labels={"Base MSRP": "Harga Dasar (USD)", "Electric Range": "Jarak Tempuh (Mil)"},
        )
        st.plotly_chart(fig_scatter)
    else:
        st.error("Kolom 'Base MSRP' atau 'Electric Range' tidak ditemukan dalam dataset.")
