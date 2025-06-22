# Project-Image-Compression-Based-on-PCA
Project Based Learning 2 : Aplikasi Nilai Eigen dan Principal Component Analysis pada Kompresi Gambar

## Anggota Kelompok 
1. Besty Mega Fauziah (L0124007)
2. Deoshi Anessah Zheren Areja (L0124009)
3. Dina Hamala Nur Rosyidah (L0124010)

## Deskripsi Program 
Kompresi gambar adalah proses untuk mengurangi ukuran file gambar dengan tetap mempertahankan kualitas visual sebanyak mungkin.
Program ini menggunakan algoritma Principal Component Analysis (PCA) untuk mengekstrak fitur utama dari gambar dan merekonstruksi citra berdasarkan sejumlah komponen utama (principal components) yang dipilih.
Pendekatan ini memungkinkan pengurangan dimensi data gambar secara efisien, menghasilkan ukuran file yang lebih kecil namun tetap menyerupai gambar asli.

## Fitur
- PCA Manual per Channel : Kompresi dilakukan secara terpisah pada masing-masing kanal warna (R, G, B) menggunakan PCA buatan sendiri (tanpa library machine learning).
- Slider Jumlah Komponen : Pengguna dapat memilih jumlah komponen PCA untuk menyesuaikan kualitas dan ukuran file hasil kompresi.
- Perbandingan Visual : Menampilkan gambar asli dan hasil kompresi secara berdampingan beserta informasi ukuran file dan efisiensi kompresi.
- Statistik Evaluasi : Menampilkan nilai MSE (Mean Squared Error) dan PSNR (Peak Signal-to-Noise Ratio) sebagai metrik kualitas kompresi.
- Unduh Gambar Kompresi : Pengguna dapat mengunduh hasil kompresi secara langsung dari aplikasi.

## Cara Penggunaan 
- Buka folder yang berisi app.py menggunakan terminal
- Jalankan command prompt "streamlit run app.py" di terminal
- Aplikasi akan terbuka otomatis di localhost
- Atur jumlah komponen PCA melalui slinder sesuai dengan kebutuhan.
- Aplikasi akan menampilkan:
a. Gambar asli dan hasil kompresi
b. Ukuran file sebelum dan sesudah
c. Estimasi pengurangan ukuran
d. Nilai MSE dan PSNR
- Klik tombol "Unduh Gambar Kompresi" untuk menyimpan hasil ke komputer.

