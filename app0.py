import streamlit as st
import pandas as pd
import joblib

# === Load Model & Scaler ===
try:
    kmeans_model = joblib.load("kmeans_model.pkl")
    scaler = joblib.load("scaler.pkl")
except FileNotFoundError:
    st.error("Model atau scaler tidak ditemukan.")
    st.stop()

# === Kolom ===
numeric_cols = ['year', 'followers', 'price_per_ml', 'size_ml']
concentration_cols = ['EDT', 'EDP', 'XDP']
full_columns = numeric_cols + concentration_cols

# === UI ===
st.title("Prediksi Klaster Produk Parfum Brand Lokal")
st.write("Silakan masukkan data secara manual:")

with st.form("form_parfum"):
    year_input = st.text_input("Tahun Rilis")
    followers_input = st.text_input("Jumlah Followers Brand")
    price_input = st.text_input("Harga per ml (Rp)")
    size_input = st.text_input("Ukuran Botol (ml)")
    concentration = st.selectbox("Konsentrasi", ['Pilih Konsentrasi', 'EDT', 'EDP', 'XDP'])
    submit = st.form_submit_button("Prediksi Klaster")

# === Proses ===
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
        # Buat input
        input_df = pd.DataFrame({
            'year': [year],
            'followers': [followers],
            'price_per_ml': [price_per_ml],
            'size_ml': [size_ml],
            'concentration': [concentration]
        })

        # Scaling
        scaled_data = scaler.transform(input_df[numeric_cols])
        scaled_df = pd.DataFrame(scaled_data, columns=numeric_cols)

        # Encoding
        encoded_concentration = pd.get_dummies(input_df['concentration'])
        for col in concentration_cols:
            if col not in encoded_concentration:
                encoded_concentration[col] = 0
        encoded_concentration = encoded_concentration[concentration_cols]

        # Final input
        final_input = pd.concat([scaled_df, encoded_concentration], axis=1)
        final_input = final_input[full_columns]

        # Prediksi
        cluster_result = kmeans_model.predict(final_input.values)[0]

        # Output
        st.subheader("Hasil Prediksi Klaster:")
        st.success(f"Parfum ini diprediksi masuk ke **Klaster {cluster_result}**")

        cluster_info = {
            0: "Klaster 0: Parfum terjangkau dan ringan.",
            1: "Klaster 1: Parfum premium dengan banyak followers.",
            2: "Klaster 2: Parfum berukuran besar dan konsentrasi tinggi.",
            3: "Klaster 3: Parfum niche atau eksperimental."
        }

        st.write("Interpretasi Klaster:")
        st.write(cluster_info.get(cluster_result, "Interpretasi belum tersedia."))

    except Exception as e:
        st.error(f"Terjadi error saat prediksi: {e}")
