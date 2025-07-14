import streamlit as st
import pandas as pd
import plotly.express as px
import os

def show():
    csv_path = r"D:\SEMESTER 4\Proyek Terintegrasi\parfum\parfum_after_cleaning.csv"

    @st.cache_data
    def load_data(path):
        if os.path.exists(path):
            return pd.read_csv(path)
        st.error("File CSV tidak ditemukan.")
        st.stop()

    df = load_data(csv_path)
    df['year'] = pd.to_numeric(df['year'], errors='coerce')

    st.title("📊 Dashboard Data Parfum Brand Lokal")

    if 'concentration' in df.columns:
        concentration_counts = df['concentration'].value_counts().reset_index()
        concentration_counts.columns = ['concentration', 'count']

        fig_pie = px.pie(
            concentration_counts,
            names='concentration',
            values='count',
            title='Distribusi Konsentrasi Parfum'
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    avg_price_per_brand = df.groupby('brand')['price'].mean().sort_values(ascending=False).head(10)
    avg_price_df = avg_price_per_brand.reset_index()

    fig_bar_price = px.bar(
        avg_price_df,
        x='brand',
        y='price',
        title='Top 10 Brands by Average Price',
        labels={'brand': 'Brand', 'price': 'Rata-rata Harga'}
    )
    fig_bar_price.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_bar_price, use_container_width=True)

    year_counts = df['year'].value_counts().sort_index().reset_index()
    year_counts.columns = ['year', 'count']

    fig_year = px.bar(
        year_counts,
        x='year',
        y='count',
        title='Distribusi Tahun Berdiri Brand',
        labels={'year': 'Tahun Berdiri', 'count': 'Jumlah Brand'}
    )
    fig_year.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_year, use_container_width=True)

    top_10_variants = df['variant'].value_counts().head(10).index.tolist()
    df_top_variants = df[df['variant'].isin(top_10_variants)]

    crosstab = pd.crosstab(df_top_variants['variant'], df_top_variants['brand'])
    crosstab = crosstab.reset_index().melt(id_vars='variant', var_name='brand', value_name='count')
    crosstab = crosstab[crosstab['count'] > 0]

    fig_variant = px.bar(
        crosstab,
        x='variant',
        y='count',
        color='brand',
        title='Number of Variants per Brand (Top 10 Variants)',
        labels={'variant': 'Varian', 'count': 'Jumlah'}
    )
    fig_variant.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_variant, use_container_width=True)
