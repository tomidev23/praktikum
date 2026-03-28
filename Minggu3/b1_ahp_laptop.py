import numpy as np

# ============================================================
# B1 - Implementasi AHP untuk Pemilihan Laptop
# Kriteria: Harga, Performa, Daya Tahan Baterai, Fitur Tambahan
# ============================================================

def ahp_method(criteria_matrix):
    """
    Menghitung bobot prioritas menggunakan metode AHP.
    Langkah:
    1. Hitung eigenvalue dan eigenvector dari matriks perbandingan
    2. Ambil eigenvector yang sesuai dengan eigenvalue terbesar (max)
    3. Normalisasi eigenvector → bobot prioritas
    """
    eigvals, eigvecs = np.linalg.eig(criteria_matrix)
    max_index = np.argmax(eigvals)
    weights = eigvecs[:, max_index]
    normalized_weights = weights / np.sum(weights)
    return normalized_weights.real

def consistency_ratio(matrix, weights):
    """
    Menghitung Consistency Ratio (CR).
    CR < 0.1 = konsisten (matriks dapat diterima).
    """
    n = len(matrix)
    # Random Index (RI) untuk n = 1..10
    RI = [0, 0, 0.58, 0.90, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49]
    
    lambda_max = np.dot(np.dot(matrix, weights), 1 / weights).mean()
    CI = (lambda_max - n) / (n - 1)
    CR = CI / RI[n - 1]
    return lambda_max, CI, CR

def score_alternatives(alt_matrix, weights):
    """
    Menghitung skor akhir setiap alternatif berdasarkan bobot kriteria.
    alt_matrix: baris = alternatif, kolom = nilai per kriteria (sudah dinormalisasi)
    """
    return alt_matrix @ weights

# ----------------------------------------------------------
# MATRIKS PERBANDINGAN KRITERIA (Saaty Scale 1–9)
# Skala: 1=sama penting, 3=sedikit lebih penting, 5=lebih penting,
#        7=jauh lebih penting, 9=mutlak lebih penting
#
# Urutan: Harga, Performa, Baterai, Fitur Tambahan
# Interpretasi: Harga dianggap paling penting (nilai 3,5,7 lebih tinggi dari kriteria lain)
# ----------------------------------------------------------
criteria_matrix = np.array([
    [1,   3,   5,   7  ],  # Harga vs (Harga, Performa, Baterai, Fitur)
    [1/3, 1,   3,   5  ],  # Performa vs ...
    [1/5, 1/3, 1,   3  ],  # Baterai vs ...
    [1/7, 1/5, 1/3, 1  ],  # Fitur vs ...
])

kriteria = ["Harga", "Performa", "Baterai", "Fitur Tambahan"]
alternatif = ["Laptop A", "Laptop B", "Laptop C"]

# Hitung bobot kriteria
weights = ahp_method(criteria_matrix)
lambda_max, CI, CR = consistency_ratio(criteria_matrix, weights)

print("=" * 50)
print("  HASIL AHP - PEMILIHAN LAPTOP")
print("=" * 50)
print("\nBobot Prioritas Kriteria:")
for k, w in zip(kriteria, weights):
    print(f"  {k:<20}: {w:.4f} ({w*100:.2f}%)")

print(f"\nConsistency Check:")
print(f"  λ max  = {lambda_max:.4f}")
print(f"  CI     = {CI:.4f}")
print(f"  CR     = {CR:.4f}  {'✓ KONSISTEN' if CR < 0.1 else '✗ Tidak Konsisten (revisi matriks)'}")

# ----------------------------------------------------------
# MATRIKS PENILAIAN ALTERNATIF PER KRITERIA
# Nilai sudah dinormalisasi (0–1), makin tinggi makin baik
# Baris = alternatif, Kolom = kriteria
# ----------------------------------------------------------
# Catatan: Untuk kriteria Harga, nilai tinggi = harga MURAH (menguntungkan)
alt_matrix = np.array([
    # Harga  Performa  Baterai  Fitur
    [0.6,    0.7,      0.8,     0.5],   # Laptop A
    [0.3,    0.9,      0.6,     0.8],   # Laptop B
    [0.8,    0.5,      0.9,     0.4],   # Laptop C
])

scores = score_alternatives(alt_matrix, weights)
ranking = np.argsort(scores)[::-1]

print("\nSkor Akhir Alternatif:")
for i in ranking:
    print(f"  {alternatif[i]:<12}: {scores[i]:.4f}")

print(f"\n→ Rekomendasi: {alternatif[ranking[0]]} adalah laptop terbaik!")