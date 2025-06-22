import streamlit as st
import numpy as np
from PIL import Image
import time
from io import BytesIO
import os
from pca_compression import PCAImageCompressor

st.set_page_config(page_title="📷 PCA Image Compression", layout="centered")
st.title("📷 Kompresi Gambar dengan PCA")

uploaded_file = st.file_uploader("Unggah gambar", type=["jpg", "jpeg", "png"])
n_components = st.slider("Jumlah komponen PCA", min_value=5, max_value=200, value=50)

if uploaded_file:
    # Baca gambar & hitung ukuran asli
    original_image = Image.open(uploaded_file).convert("RGB")
    image_array = np.array(original_image)

    uploaded_file.seek(0, os.SEEK_END)
    original_size_kb = uploaded_file.tell() / 1024
    uploaded_file.seek(0)

    # Kompres gambar
    compressor = PCAImageCompressor()
    start_time = time.time()
    compressed_array = compressor.compress_image_pca(image_array, n_components)
    runtime = time.time() - start_time
    compressed_image = Image.fromarray(compressed_array)

    # Hitung ukuran hasil kompresi
    img_buffer = BytesIO()
    compressed_image.save(img_buffer, format="JPEG", quality=85)
    compressed_size_kb = len(img_buffer.getvalue()) / 1024

    # Tampilkan gambar sejajar
    col1, col2 = st.columns(2)

    with col1:
        st.image(original_image, caption="🖼️ Gambar Asli", use_container_width=True)
        st.write(f"📦 Ukuran Asli: `{original_size_kb:.2f} KB`")

    with col2:
        st.image(compressed_image, caption="🗜️ Gambar Setelah Kompresi", use_container_width=True)
        st.write(f"📦 Ukuran Kompresi: `{compressed_size_kb:.2f} KB`")

    # Estimasi pengurangan ukuran
    compression_rate = 100 * (1 - (compressed_size_kb / original_size_kb))
    st.write(f"📉 Estimasi Pengurangan Ukuran: `{compression_rate:.2f}%`")
    st.write(f"🕒 Waktu Proses: `{runtime:.3f}` detik")

    # 🔍 Tampilkan hasil kompresi (MSE dan PSNR)
    stats = compressor.get_stats()
    st.subheader("📊 Hasil Kompresi PCA")
    st.write(f"- 🔢 MSE (Mean Squared Error): `{stats['mse']:.4f}`")
    st.write(f"- 🔊 PSNR (Peak Signal-to-Noise Ratio): `{stats['psnr']:.2f} dB`")
    st.write(f"- 🧩 Komponen PCA yang Digunakan: `{stats['components']}`")

    # Tombol unduh
    st.download_button("📥 Unduh Gambar Kompresi", img_buffer.getvalue(),
                       file_name="compressed.png", mime="image/png")
