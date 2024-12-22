# File: streamlit_fpb_growth_chart.py

import streamlit as st
import timeit
import matplotlib.pyplot as plt

# Fungsi FPB iteratif
def fpb_iterative(a, b):
    while b:
        a, b = b, a % b
    return a

# Fungsi FPB rekursif
def fpb_recursive(a, b):
    if b == 0:
        return a
    return fpb_recursive(b, a % b)

# Fungsi untuk mengukur waktu eksekusi
def measure_time(func, a, b):
    return timeit.timeit(lambda: func(a, b), number=1)

# Streamlit layout
st.title("Grafik Pertumbuhan Algoritma FPB")
st.write(
    "Aplikasi ini menghitung FPB menggunakan algoritma rekursif dan iteratif, "
    "dengan nilai `a` tetap dan daftar nilai `b` yang dapat diinputkan bebas oleh pengguna."
)

# Input pengguna
a = st.number_input("Masukkan nilai tetap untuk a:", min_value=1, value=100, step=1, format="%d")
b_input = st.text_area(
    "Masukkan daftar nilai untuk b (pisahkan dengan koma):",
    value="10,20,30,40,50",
    help="Contoh: 10,20,30,40,50",
)

if st.button("Hitung FPB"):
    try:
        # Parsing input b
        b_values = list(map(int, b_input.split(',')))
        if not b_values:
            st.error("Masukkan setidaknya satu nilai untuk b.")
        else:
            # Inisialisasi data
            iter_times = []
            recur_times = []

            # Hitung waktu eksekusi untuk setiap nilai b
            for b in b_values:
                time_iter = measure_time(fpb_iterative, a, b)
                time_recur = measure_time(fpb_recursive, a, b)

                iter_times.append(time_iter)
                recur_times.append(time_recur)

            # Konversi satuan waktu
            max_time = max(max(iter_times), max(recur_times))
            if max_time < 1:
                # Jika waktu eksekusi sangat kecil, gunakan milidetik
                iter_times = [t * 1000 for t in iter_times]
                recur_times = [t * 1000 for t in recur_times]
                time_unit = "milidetik"
            else:
                # Jika waktu cukup besar, gunakan detik
                time_unit = "detik"

            # Tampilkan detail waktu eksekusi dalam tabel
            st.subheader("Tabel Waktu Eksekusi")
            results_table = {
                "Nilai b": b_values,
                f"Iteratif ({time_unit})": [f"{t:.6f}" for t in iter_times],
                f"Rekursif ({time_unit})": [f"{t:.6f}" for t in recur_times],
            }
            st.table(results_table)

            # Visualisasi grafik pertumbuhan
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(b_values, recur_times, label="Rekursif", color="yellow", marker="o")
            ax.plot(b_values, iter_times, label="Iteratif", color="black", marker="o")

            # Anotasi dan pengaturan grafik
            ax.set_title("Grafik Pertumbuhan Waktu Eksekusi Algoritma FPB", fontsize=16)
            ax.set_xlabel("Nilai b (ukuran input)", fontsize=14)
            ax.set_ylabel(f"Waktu Eksekusi ({time_unit})", fontsize=14)
            ax.legend(fontsize=12)
            ax.grid(linestyle="--", alpha=0.7)

            # Tampilkan grafik
            st.pyplot(fig)

    except ValueError:
        st.error("Input tidak valid. Pastikan Anda memasukkan nilai b yang dipisahkan dengan koma.")
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")

# Footer
st.write("💡 **Tips**: Masukkan nilai `b` sebanyak mungkin untuk melihat perbandingan kinerja secara mendetail.")
