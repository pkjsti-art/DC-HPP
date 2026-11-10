import streamlit as st

def load_cyber_css():
    """Menginjeksi Custom CSS untuk tema Galaxy dengan Sidebar Cozy & Seamless"""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

        /* Latar Belakang Utama - Galaxy Radial Gradient */
        .stApp {
            background: radial-gradient(circle at 15% 10%, #1a0b2e 0%, #0b0f19 40%, #05020a 100%) !important;
            color: #E2E8F0;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }
        
        /* Sidebar Cozy & Seamless (Sangat transparan, garis batas sangat halus) */
        [data-testid="stSidebar"] {
            background-color: rgba(10, 5, 20, 0.15) !important;
            backdrop-filter: blur(25px) !important;
            -webkit-backdrop-filter: blur(25px) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.03) !important;
        }
        
        /* Beri jarak atas agar menu tidak terlalu mepet dengan ujung layar */
        [data-testid="stSidebar"] > div:first-child {
            padding-top: 3rem;
        }

        /* --- ROMBAK TOTAL MENU NAVIGASI (RADIO BUTTONS) --- */
        /* 1. Sembunyikan lingkaran (bullet) bawaan */
        div[role="radiogroup"] > label > div:first-child {
            display: none !important;
        }
        
        /* 2. Desain tab menu yang cozy dan mulus */
        div[role="radiogroup"] label {
            background: transparent;
            border: none !important;
            border-radius: 12px;
            padding: 14px 20px;
            margin-bottom: 8px;
            color: #94A3B8;
            font-weight: 500;
            font-size: 1.05rem;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        /* 3. Efek Hover (Bergeser lembut ke kanan saat disentuh kursor) */
        div[role="radiogroup"] label:hover {
            background: rgba(168, 85, 247, 0.08);
            color: #d8b4fe;
            transform: translateX(6px);
        }
        
        /* 4. Menu Aktif (Selected) - Glow lembut di sebelah kiri */
        div[role="radiogroup"] label[data-selected="true"] {
            background: linear-gradient(90deg, rgba(168, 85, 247, 0.15) 0%, rgba(0,0,0,0) 100%) !important;
            border-left: 4px solid #c084fc !important;
            color: #ffffff !important;
            font-weight: 600;
            box-shadow: none !important;
        }
        /* -------------------------------------------------- */
        
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
