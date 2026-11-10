import streamlit as st

def load_cyber_css():
    """Menginjeksi Custom CSS untuk tema Galaxy, Glassmorphism, dan Panel Transparan"""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

        /* Latar Belakang Utama - Galaxy Radial Gradient */
        .stApp {
            background: radial-gradient(circle at 15% 10%, #1a0b2e 0%, #0b0f19 40%, #05020a 100%) !important;
            color: #E2E8F0;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }
        
        /* Sidebar dengan efek kaca (Glassmorphism) dan blur transparan */
        [data-testid="stSidebar"] {
            background-color: rgba(10, 5, 20, 0.4) !important;
            backdrop-filter: blur(16px) !important;
            -webkit-backdrop-filter: blur(16px) !important;
            border-right: 1px solid rgba(138, 43, 226, 0.2) !important;
        }
        
        /* Teks Sidebar */
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2 {
            color: #c084fc !important;
            text-shadow: 0 0 15px rgba(192, 132, 252, 0.4);
            font-weight: 600;
        }

        /* Tombol Navigasi Sidebar */
        div[role="radiogroup"] label {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            padding: 10px 15px;
            margin-bottom: 10px;
            color: #94A3B8;
            transition: all 0.3s ease;
        }
        div[role="radiogroup"] label:hover {
            border-color: rgba(192, 132, 252, 0.4);
            background: rgba(192, 132, 252, 0.05);
            color: #e879f9;
        }
        div[role="radiogroup"] label[data-selected="true"] {
            background: linear-gradient(90deg, rgba(139, 92, 246, 0.15) 0%, rgba(0, 0, 0, 0) 100%);
            border-left: 3px solid #a855f7;
            border-color: rgba(168, 85, 247, 0.2);
            color: #f3e8ff !important;
            box-shadow: inset 10px 0 20px -10px rgba(168, 85, 247, 0.2);
        }
        
        /* Tombol Utama (Aksi) - Gradasi Transparan bercahaya */
        .stButton>button {
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.7) 0%, rgba(59, 130, 246, 0.7) 100%) !important;
            backdrop-filter: blur(5px);
            color: #FFFFFF !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 12px !important;
            padding: 0.6rem 1.5rem !important;
            font-weight: 600 !important;
            letter-spacing: 0.5px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(139, 92, 246, 0.2) !important;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(139, 92, 246, 0.4) !important;
            border-color: rgba(255, 255, 255, 0.4) !important;
            background: linear-gradient(135deg, rgba(168, 85, 247, 0.85) 0%, rgba(96, 165, 250, 0.85) 100%) !important;
        }
        
        /* Judul Terpusat dengan Teks Gradasi Galaxy */
        .custom-title-container {
            text-align: center;
            padding: 1.5rem 0 2rem 0;
        }
        .custom-title {
            background: linear-gradient(to right, #60a5fa, #c084fc, #f472b6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.6rem !important;
            font-weight: 700;
            letter-spacing: -0.5px;
            margin: 0;
            text-shadow: 0 10px 30px rgba(192, 132, 252, 0.15);
        }
        .custom-subtitle {
            color: #94a3b8;
            font-size: 1.1rem;
            font-weight: 300;
            margin-top: 8px;
        }
        
        /* Box Notifikasi / Upload File - Efek Kaca Transparan */
        div[data-testid="stInfo"], div[data-testid="stWarning"], div[data-testid="stError"], div[data-testid="stSuccess"], div[data-testid="stFileUploader"] > section {
            background: rgba(30, 41, 59, 0.3) !important;
            backdrop-filter: blur(12px) !important;
            border-radius: 12px !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }
        
        /* KPI Card (Metrik) - Glassmorphism Galaxy */
        div[data-testid="stMetric"] {
            background: rgba(15, 23, 42, 0.4) !important;
            backdrop-filter: blur(16px) !important;
            -webkit-backdrop-filter: blur(16px) !important;
            border: 1px solid rgba(139, 92, 246, 0.15) !important;
            border-top: 2px solid #a855f7 !important;
            padding: 1.5rem;
            border-radius: 16px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
            transition: transform 0.3s ease, border-color 0.3s ease;
        }
        div[data-testid="stMetric"]:hover {
            transform: translateY(-5px);
            border-color: rgba(168, 85, 247, 0.4) !important;
            box-shadow: 0 12px 40px rgba(139, 92, 246, 0.15);
        }
        div[data-testid="stMetricLabel"] {
            color: #cbd5e1 !important;
            font-weight: 500 !important;
            letter-spacing: 0.5px;
        }
        div[data-testid="stMetricValue"] {
            background: linear-gradient(to right, #93c5fd, #d8b4fe);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700 !important;
            font-size: 2rem !important;
        }
        </style>
    """, unsafe_allow_html=True)

def render_kpi_metrics(total_data, max_naik, max_turun):
    """Menampilkan ringkasan metrik di atas dashboard"""
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="✨ TOTAL DATA PROSES", value=f"{total_data:,}")
    with col2:
        st.metric(label="📈 LONJAKAN TERTINGGI", value=f"+{max_naik}%")
    with col3:
        st.metric(label="📉 PENURUNAN TERDALAM", value=f"{max_turun}%")
