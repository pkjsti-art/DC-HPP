import streamlit as st

def load_cyber_css():
    """Menginjeksi Custom CSS untuk tema Cyber, Futuristik, IT, Server"""
    st.markdown("""
        <style>
        /* Background & Teks Utama */
        .stApp {
            background-color: #0B0F19; /* Biru sangat gelap / hitam server */
            color: #E2E8F0;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #111827;
            border-right: 1px solid #1D4ED8;
        }
        
        /* Tombol Futuristik */
        .stButton>button {
            background: linear-gradient(90deg, #1D4ED8 0%, #3B82F6 100%);
            color: white;
            border: none;
            border-radius: 4px;
            padding: 0.5rem 1rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px -1px rgba(29, 78, 216, 0.3);
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(29, 78, 216, 0.4);
            border-color: #60A5FA;
        }
        
        /* Header & Judul */
        h1, h2, h3 {
            color: #60A5FA !important;
            font-family: 'Courier New', Courier, monospace; /* Kesan koding/IT */
        }
        
        /* Kotak Notifikasi / Metrik */
        div[data-testid="stMetric"] {
            background-color: #1E293B;
            border-left: 4px solid #3B82F6;
            padding: 1rem;
            border-radius: 4px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        </style>
    """, unsafe_allow_html=True)

def render_kpi_metrics(total_data, max_naik, max_turun):
    """Menampilkan ringkasan metrik di atas dashboard"""
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Baris Diproses", value=total_data)
    with col2:
        st.metric(label="Lonjakan Tertinggi", value=f"{max_naik}%")
    with col3:
        st.metric(label="Penurunan Terdalam", value=f"{max_turun}%")
