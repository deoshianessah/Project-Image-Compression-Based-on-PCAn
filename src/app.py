import streamlit as st
import numpy as np
from PIL import Image
import time
from io import BytesIO
import os
from pca_compression import PCAImageCompressor

# --- Custom Page Settings ---
st.set_page_config(page_title="📷 PCA Image Compression", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background-color: #0a1930;
        color: white;
        font-family: 'Segoe UI', sans-serif;
    }
    h1, h2, h3, .stMarkdown, .stSlider, .stButton, .stTextInput, .stDownloadButton {
        color: white !important;
    }
    .stSlider > div > div {
        color: white;
    }
    .stTabs [role="tab"] {
        background-color: #102944;
        color: white;
        border-radius: 5px 5px 0 0;
        padding: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #145DA0;
        font-weight: bold;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# --- Judul Aplikasi ---
st.markdown("<h1 style='text-align: center;'>📷 Kompresi Gambar dengan PCA</h1>", unsafe_allow_html=True)
st.markdown("<hr style='border-color: #145DA0;'>", unsafe_allow_html=True)

# --- Input ---
uploaded_file = st.file_uploader("Unggah gambar", type=["jpg", "jpeg", "png"])
n_components = st.slider("Jumlah komponen PCA", min_value=5, max_value=200, value=100)

if uploaded_file:
    # Proses Gambar
    original_image = Image.open(uploaded_file).convert("RGB")
    image_array = np.array(original_image)

    uploaded_file.seek(0, os.SEEK_END)
    original_size_kb = uploaded_file.tell() / 1024
    uploaded_file.seek(0)

    with st.spinner("🔄 Sedang mengompresi gambar..."):
        compressor = PCAImageCompressor()
        start_time = time.time()
        compressed_array = compressor.compress_image_pca(image_array, n_components)
        runtime = time.time() - start_time
        compressed_image = Image.fromarray(compressed_array)

    # Ukuran kompresi
    img_buffer = BytesIO()
    compressed_image.save(img_buffer, format="JPEG", quality=85)
    compressed_size_kb = len(img_buffer.getvalue()) / 1024

    compression_rate = 100 * (1 - (compressed_size_kb / original_size_kb))
    stats = compressor.get_stats()

    # --- Tabs UI ---
    tab1, tab2, tab3 = st.tabs(["📷 Gambar", "📊 Statistik", "📥 Unduh"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.image(original_image, caption="🖼️ Gambar Asli", use_container_width=True)
            st.write(f"📦 Ukuran Asli: `{original_size_kb:.2f} KB`")
        with col2:
            st.image(compressed_image, caption="🗜️ Gambar Setelah Kompresi", use_container_width=True)
            st.write(f"📦 Ukuran Kompresi: `{compressed_size_kb:.2f} KB`")

    with tab2:
        st.markdown("### 📉 Statistik Kompresi PCA")
        st.metric("📏 Estimasi Pengurangan", f"{compression_rate:.2f}%")
        st.metric("🕒 Waktu Proses", f"{runtime:.3f} detik")
        st.metric("🔢 MSE", f"{stats['mse']:.4f}")
        st.metric("🔊 PSNR", f"{stats['psnr']:.2f} dB")
        st.metric("🧩 Komponen PCA", stats['components'])

    with tab3:
        st.markdown("### 📥 Unduh Gambar")
        st.download_button("💾 Unduh Gambar Kompresi", img_buffer.getvalue(),
                           file_name="compressed.png", mime="image/png")

# --- Footer ---
st.markdown("""
    <hr>
    <p style='text-align:center; color:gray;'>
    Dibuat dengan oleh <strong>Kelompok 6</strong> | 2025
    </p>
""", unsafe_allow_html=True)