import streamlit as st

def load_cyber_css():
    """Menginjeksi Custom CSS untuk tema Cyber, Futuristik, IT, Server bernuansa Dark-Amber/Oranye"""
    st.markdown("""
        <style>
        /* Impor font Cyber/Modern */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

        /* Background & Teks Utama */
        .stApp {
            background: linear-gradient(135deg, #0A0C10 0%, #111318 100%); /* Gelap pekat */
            color: #E2E8F0;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }
        
        /* Sidebar styling futuristik (Gelap pekat dengan aksen oranye di perbatasan) */
        [data-testid="stSidebar"] {
            background-color: #07090C !important;
            border-right: 2px solid #E879F9; /* Garis tipis cyber glow */
            border-image: linear-gradient(to bottom, #EA580C, #1E1B4B) 1;
        }
        
        /* Styling Sidebar Text */
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2 {
            font-family: 'Space Grotesk', sans-serif;
            color: #F97316 !important; /* Cyber Orange */
            text-shadow: 0 0 10px rgba(249, 115, 22, 0.2);
        }

        /* Radio buttons di Sidebar */
        div[role="radiogroup"] label {
            background: #11141A;
            border: 1px solid #1F2937;
            border-radius: 8px;
            padding: 8px 12px;
            margin-bottom: 8px;
            color: #94A3B8;
            font-weight: 500;
            transition: all 0.2s ease-in-out;
        }
        div[role="radiogroup"] label:hover {
            border-color: #EA580C;
            color: #F97316;
            transform: translateX(2px);
        }
        div[role="radiogroup"] label[data-selected="true"] {
            background: linear-gradient(90deg, rgba(234, 88, 12, 0.15) 0%, rgba(0, 0, 0, 0) 100%);
            border-color: #F97316;
            color: #FFEDD5 !important;
            box-shadow: 0 0 15px rgba(249, 115, 22, 0.1);
        }
        
        /* Tombol Futuristik Oranye Gradasi */
        .stButton>button {
            background: linear-gradient(90deg, #EA580C 0%, #FF7E33 100%) !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.6rem 1.5rem !important;
            font-weight: 700 !important;
            font-family: 'Space Grotesk', sans-serif;
            letter-spacing: 0.5px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 14px rgba(234, 88, 12, 0.3) !important;
        }
        .stButton>button:hover {
            transform: translateY(-2px) scale(1.01);
            box-shadow: 0 6px 20px rgba(234, 88, 12, 0.5) !important;
            border-color: #FFA559 !important;
        }
        
        /* Judul, Header & Subheader di Tengah */
        .custom-title-container {
            text-align: center; /* Meratakan ke tengah */
            padding: 1.5rem 0 2rem 0;
            font-family: 'Space Grotesk', sans-serif;
        }
        .custom-title {
            background: linear-gradient(90deg, #F97316 0%, #FDBA74 50%, #EA580C 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.8rem !important;
            font-weight: 800;
            letter-spacing: -1px;
            text-transform: uppercase;
            margin: 0;
            text-shadow: 0 0 30px rgba(249, 115, 22, 0.15);
        }
        .custom-subtitle {
            color: #64748B;
            font-size: 1rem;
            font-weight: 400;
            margin-top: 5px;
        }
        
        /* Box Informasi / Kotak Info bertekstur dashboard */
        div[data-testid="stInfo"], div[data-testid="stWarning"], div[data-testid="stError"], div[data-testid="stSuccess"] {
            background-color: #0E1116 !important;
            border-radius: 12px !important;
            border: 1px solid #1F2937 !important;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.5);
        }
        
        /* Kotak Notifikasi / Metrik Dashboard Gelap */
        div[data-testid="stMetric"] {
            background-color: #0E1116;
            border: 1px solid #1E293B;
            border-left: 4px solid #EA580C !important; /* Neon Amber Glow Border */
            padding: 1.25rem;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            transition: transform 0.2s;
        }
        div[data-testid="stMetric"]:hover {
            transform: translateY(-3px);
            border-color: #EA580C;
        }
        div[data-testid="stMetricLabel"] {
            color: #94A3B8 !important;
            font-weight: 600 !important;
        }
        div[data-testid="stMetricValue"] {
            color: #F97316 !important;
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 700 !important;
        }
        </style>
    """, unsafe_allow_html=True)

def render_kpi_metrics(total_data, max_naik, max_turun):
    """Menampilkan ringkasan metrik di atas dashboard"""
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="📊 TOTAL DATA PROSES", value=f"{total_data:,}")
    with col2:
        st.metric(label="📈 LONJAKAN TERTINGGI", value=f"+{max_naik}%")
    with col3:
        st.metric(label="📉 PENURUNAN TERDALAM", value=f"{max_turun}%")
