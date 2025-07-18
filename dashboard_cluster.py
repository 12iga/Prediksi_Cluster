import streamlit as st
import plotly.express as px
from logic import fetch_all_predictions

def show():

    st.title("🔍 Dashboard Hasil Prediksi Klaster Parfum")

    # Ambil data dari database
    df = fetch_all_predictions()

    # Validasi
    if df.empty:
        st.warning("Belum ada data prediksi yang tersimpan.")
        st.stop()

    # --- Filter Klaster ---
    cluster_list = sorted(df['cluster'].unique())
    selected_cluster = st.selectbox("Pilih Klaster (atau lihat semua)", options=["Semua"] + cluster_list)

    # Filter data jika klaster dipilih
    if selected_cluster != "Semua":
        df = df[df['cluster'] == selected_cluster]

    # --- PIE CHART: Jumlah Produk per Klaster ---
    cluster_counts = df['cluster'].value_counts().reset_index()
    cluster_counts.columns = ['cluster', 'count']

    fig_pie_cluster = px.pie(
        cluster_counts,
        names='cluster',
        values='count',
        title='Presentase Jumlah Brand Produk Parfum per Klaster',
        labels={'cluster': 'Klaster', 'count': 'Jumlah'}
    )
    st.plotly_chart(fig_pie_cluster, use_container_width=True)

    # --- BAR CHART: Rata-Rata Followers per Klaster ---
    avg_followers = df.groupby('cluster')['followers'].mean().reset_index()

    fig_bar_followers = px.bar(
        avg_followers,
        x='cluster',
        y='followers',
        title='Rata-rata Followers per Klaster',
        labels={'cluster': 'Klaster', 'followers': 'Followers'}
    )
    st.plotly_chart(fig_bar_followers, use_container_width=True)

    # --- BAR CHART: Rata-Rata Price per ml per Klaster ---
    avg_price = df.groupby('cluster')['price_per_ml'].mean().reset_index()

    fig_bar_price = px.bar(
        avg_price,
        x='cluster',
        y='price_per_ml',
        title='Rata-rata Price per ml per Klaster',
        labels={'cluster': 'Klaster', 'price_per_ml': 'Price per ml'}
    )
    st.plotly_chart(fig_bar_price, use_container_width=True)

    # --- BAR CHART: Rata-Rata Size per Klaster ---
    avg_size = df.groupby('cluster')['size'].mean().reset_index()

    fig_bar_size = px.bar(
        avg_size,
        x='cluster',
        y='size',
        title='Rata-rata Size (ml) per Klaster',
        labels={'cluster': 'Klaster', 'size': 'Ukuran (ml)'}
    )
    st.plotly_chart(fig_bar_size, use_container_width=True)

    # --- PIE CHART: Konsentrasi Parfum per Klaster ---
    if 'concentration' in df.columns:
        concentration_counts = df['concentration'].value_counts().reset_index()
        concentration_counts.columns = ['concentration', 'count']

        fig_pie_conc = px.pie(
            concentration_counts,
            names='concentration',
            values='count',
            title='Distribusi Konsentrasi Parfum',
            labels={'concentration': 'Konsentrasi', 'count': 'Jumlah'}
        )
        st.plotly_chart(fig_pie_conc, use_container_width=True)

    # --- BAR CHART: Rata-Rata Tahun Berdiri per Klaster ---
    if 'year' in df.columns:
        avg_year = df.groupby('cluster')['year'].mean().reset_index()

        fig_bar_year = px.bar(
            avg_year,
            x='cluster',
            y='year',
            title='Rata-rata Tahun Berdiri per Klaster',
            labels={'cluster': 'Klaster', 'year': 'Tahun'}
        )
        st.plotly_chart(fig_bar_year, use_container_width=True)

    # --- TABEL DATA ---
    st.subheader("📄 Tabel Data Prediksi")
    st.dataframe(df.reset_index(drop=True))
