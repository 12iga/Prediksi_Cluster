import streamlit as st
from streamlit_option_menu import option_menu

import Home
import dashboard_awal
import dashboard_cluster
import statistik

st.set_page_config(page_title="Aplikasi Prediksi Parfum", layout="wide")

def main():
    with st.sidebar:
        selected = option_menu(
            menu_title="Menu",
            options=["Home", "Dashboard", "Statistik Klaster"],
            icons=["house", "bar-chart", "graph-up"],
            default_index=0,
        )

        # Jika Dashboard, munculkan selectbox submenu
        dashboard_option = None
        if selected == "Dashboard":
            dashboard_option = st.selectbox(
                "Pilih Dashboard:",
                ["Dashboard Awal", "Dashboard Cluster"]
            )

    # Routing berdasarkan pilihan menu
    if selected == "Home":
        Home.show()
    elif selected == "Dashboard":
        if dashboard_option == "Dashboard Awal":
            dashboard_awal.show()
        elif dashboard_option == "Dashboard Cluster":
            dashboard_cluster.show()
    elif selected == "Statistik Klaster":
        statistik.show()

if __name__ == "__main__":
    main()
