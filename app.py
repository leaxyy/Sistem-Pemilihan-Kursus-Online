# Streamlit Web App for SMART and SPI with User Input and CSV Upload (Enhanced UI)
import streamlit as st
import pandas as pd
import base64

# Apply page config
st.set_page_config(page_title="Evaluasi Kursus Online", layout="wide")

# Custom CSS for better UI
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
        padding: 2rem;
        border-radius: 10px;
    }
    .stButton>button {
        width: 100%;
        font-weight: bold;
    }
    .css-18ni7ap { 
        padding: 1.5rem;
        border-radius: 15px;
        background-color: white;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Inisialisasi session state
if 'platforms' not in st.session_state:
    st.session_state.platforms = []

st.title("📊 Evaluasi Platform Kursus Online dengan SMART & SPI")
st.markdown("Gunakan metode <b>SMART</b> atau <b>SPI</b> untuk menilai dan membandingkan platform kursus online.", unsafe_allow_html=True)

# Sidebar opsi input
st.sidebar.header("🔧 Metode Input Data")
input_mode = st.sidebar.radio("Pilih Metode:", ["Manual", "Upload CSV"])

# Manual Input
if input_mode == "Manual":
    st.subheader("📝 Form Input Platform Kursus Baru")

    with st.form("form_platform"):
        col1, col2, col3 = st.columns(3)
        with col1:
            name = st.text_input("Nama Platform")
            price = st.number_input("Harga per Bulan (Rp)", min_value=0)
        with col2:
            courses = st.number_input("Jumlah Kursus", min_value=0)
            quality = st.slider("Kualitas Pengajar", 0, 100, 80)
        with col3:
            cert = st.checkbox("Menyediakan Sertifikat?", value=True)
            access = st.slider("Kemudahan Akses", 0, 100, 85)

        submitted = st.form_submit_button("+ Tambah Platform")

        if submitted:
            st.session_state.platforms.append({
                "Platform": name,
                "Harga_per_Bulan": price,
                "Jumlah_Kursus": courses,
                "Kualitas_Pengajar": quality,
                "Sertifikat": int(cert),
                "Kemudahan_Akses": access
            })
            st.success(f"✅ Data platform '{name}' berhasil ditambahkan!")

# CSV Upload
else:
    st.subheader("📁 Upload File CSV Platform Kursus")
    uploaded_file = st.file_uploader("Upload file CSV", type=["csv"])
    if uploaded_file is not None:
        try:
            df_uploaded = pd.read_csv(uploaded_file)
            st.session_state.platforms = df_uploaded.to_dict(orient='records')
            st.success("✅ Data berhasil dimuat dari file CSV!")
        except Exception as e:
            st.error(f"❌ Gagal membaca file CSV: {e}")

# Proses dan tampilkan hasil jika data tersedia
if st.session_state.platforms:
    df = pd.DataFrame(st.session_state.platforms)
    st.subheader("📄 Data Platform Saat Ini")
    st.dataframe(df, use_container_width=True)

    # Define criteria weights and types
    weights = {
        'Harga_per_Bulan': 0.25,   # Cost
        'Jumlah_Kursus': 0.20,     # Benefit
        'Kualitas_Pengajar': 0.25, # Benefit
        'Sertifikat': 0.15,        # Benefit
        'Kemudahan_Akses': 0.15    # Benefit
    }

    types = {
        'Harga_per_Bulan': 'cost',
        'Jumlah_Kursus': 'benefit',
        'Kualitas_Pengajar': 'benefit',
        'Sertifikat': 'benefit',
        'Kemudahan_Akses': 'benefit'
    }

    # SMART Method
    def smart_method(df):
        df_smart = df.copy()
        for col in weights:
            if types[col] == 'benefit':
                df_smart[col + '_norm'] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())
            else:
                df_smart[col + '_norm'] = (df[col].max() - df[col]) / (df[col].max() - df[col].min())
        df_smart['SMART_Score'] = sum(df_smart[col + '_norm'] * weight for col, weight in weights.items())
        return df_smart[['Platform', 'SMART_Score']].sort_values(by='SMART_Score', ascending=False)

    # SPI Method
    def spi_method(df):
        df_spi = df.copy()
        for col in weights:
            if types[col] == 'benefit':
                df_spi[col + '_spi'] = df[col] / df[col].max()
            else:
                df_spi[col + '_spi'] = df[col].min() / df[col]
        df_spi['SPI_Score'] = sum(df_spi[col + '_spi'] * weight for col, weight in weights.items())
        return df_spi[['Platform', 'SPI_Score']].sort_values(by='SPI_Score', ascending=False)

    st.subheader("📈 Hasil Perhitungan Skor")
    metode = st.radio("Pilih Metode Penilaian:", ["SMART", "SPI"], horizontal=True)

    if metode == "SMART":
        st.write("### 🌟 Hasil SMART")
        st.dataframe(smart_method(df), use_container_width=True)
    else:
        st.write("### ⚙️ Hasil SPI")
        st.dataframe(spi_method(df), use_container_width=True)
else:
    st.info("ℹ️ Masukkan atau unggah setidaknya satu data platform untuk memulai perhitungan.")
