import streamlit as st
import pandas as pd
import joblib
from logic import save_to_database, fetch_all_predictions

def show():
    try:
        kmeans_model = joblib.load("kmeans_model.pkl")
        scaler = joblib.load("scaler.pkl")
    except FileNotFoundError:
        st.error("Model atau scaler tidak ditemukan.")
        st.stop()

    numeric_cols = ['year', 'followers', 'price_per_ml', 'size_ml']
    concentration_cols = ['EDT', 'EDP', 'XDP']
    full_columns = numeric_cols + concentration_cols

    st.title("🌸 Prediksi Klaster Produk Parfum Brand Lokal")

    with st.form("form_parfum"):
        year_input = st.number_input("Tahun Rilis", step=1, format="%d")
        followers_input = st.number_input("Jumlah Followers Brand", min_value=0, step=1, format="%d")
        price_input = st.text_input("Harga per ml (Rp)")
        size_input = st.text_input("Ukuran Botol (ml)")
        concentration = st.selectbox("Konsentrasi", ['Pilih Konsentrasi', 'EDT', 'EDP', 'XDP'])
        submit = st.form_submit_button("Prediksi Klaster")

    if submit:
        try:
            year = int(year_input)
            followers = int(followers_input)
            price_per_ml = float(price_input)
            size_ml = float(size_input)
        except:
            st.warning("Semua input numerik wajib diisi dengan angka yang valid.")
            st.stop()

        if concentration == 'Pilih Konsentrasi':
            st.warning("Pilih salah satu konsentrasi parfum.")
            st.stop()

        try:
            input_df = pd.DataFrame({
                'year': [year],
                'followers': [followers],
                'price_per_ml': [price_per_ml],
                'size_ml': [size_ml],
                'concentration': [concentration]
            })

            scaled = scaler.transform(input_df[numeric_cols])
            scaled_df = pd.DataFrame(scaled, columns=numeric_cols)

            encoded = pd.get_dummies(input_df['concentration'])
            for col in concentration_cols:
                if col not in encoded:
                    encoded[col] = 0
            encoded = encoded[concentration_cols]

            final_input = pd.concat([scaled_df, encoded], axis=1)
            final_input = final_input[full_columns]

            cluster_result = kmeans_model.predict(final_input.values)[0]

            st.subheader("Hasil Prediksi Klaster:")
            st.success(f"Parfum ini masuk ke **Klaster {cluster_result}**")

            st.write({
                0: "Klaster 0: Expert.",
                1: "Klaster 1: Beginner.",
                2: "Klaster 2: Medium.",
                3: "Klaster 3: Luxury."
            }.get(cluster_result, "Tidak dikenali."))

            save_to_database({
                'year': year,
                'followers': followers,
                'price_per_ml': price_per_ml,
                'size': size_ml,
                'concentration': concentration
            }, cluster_result)

            st.info("Data berhasil disimpan ke database.")

        except Exception as e:
            st.error(f"Error saat prediksi: {e}")

    st.markdown("---")
    st.subheader("📦 Data Prediksi Tersimpan")
    if st.button("Tampilkan Data dari Database"):
        try:
            df = fetch_all_predictions()
            if df.empty:
                st.info("Belum ada data.")
            else:
                st.dataframe(df)
        except Exception as e:
            st.error(f"Gagal mengambil data: {e}")
