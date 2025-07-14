import streamlit as st
import pandas as pd
import os

def show():
    @st.cache_data
    def load_data():
        if os.path.exists("hasil_clustering_parfum_brand.csv"):
            return pd.read_csv("hasil_clustering_parfum_brand.csv")
        st.error("File CSV hasil clustering belum ditemukan.")
        st.stop()

    def reconstruct_concentration(df):
        def get_conc(row):
            if row.get('EDT', 0) == 1:
                return 'EDT'
            elif row.get('EDP', 0) == 1:
                return 'EDP'
            elif row.get('XDP', 0) == 1:
                return 'XDP'
            else:
                return 'Unknown'
        df['concentration'] = df.apply(get_conc, axis=1)
        return df

    df = load_data()
    df = reconstruct_concentration(df)

    st.title("📈 Statistik Deskriptif Tiap Klaster Parfum")

    cluster_options = sorted(df['cluster'].unique())
    selected_cluster = st.selectbox("Pilih Klaster", cluster_options)

    subset = df[df['cluster'] == selected_cluster]

    st.markdown(f"### Statistik Deskriptif untuk Klaster {selected_cluster}")
    st.dataframe(subset.drop(columns=["cluster"]).describe())

    st.markdown("### Distribusi Konsentrasi")
    st.bar_chart(subset['concentration'].value_counts())
