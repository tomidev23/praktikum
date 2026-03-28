import numpy as np
from sklearn.preprocessing import MinMaxScaler

# ============================================================
# B2 - Implementasi TOPSIS untuk Rekomendasi Hotel
# Kriteria: Harga, Fasilitas, Jarak ke Kota, Ulasan Pelanggan
# ============================================================

def topsis(matrix, weights, benefit_criteria):
    """
    Implementasi TOPSIS (Technique for Order of Preference
    by Similarity to Ideal Solution).

    Parameter:
    - matrix         : array (m x n), baris=alternatif, kolom=kriteria
    - weights        : bobot tiap kriteria (jumlah harus = 1)
    - benefit_criteria: list bool, True=benefit (makin besar makin baik),
                        False=cost (makin kecil makin baik)

    Langkah:
    1. Normalisasi matriks (MinMax → [0,1])
    2. Kalikan dengan bobot → weighted normalized matrix
    3. Tentukan ideal positif (A+) dan ideal negatif (A-)
    4. Hitung jarak ke A+ dan A-
    5. Hitung skor preferensi: S = D- / (D+ + D-)
    """
    # Step 1 - Normalisasi
    scaler = MinMaxScaler()
    norm_matrix = scaler.fit_transform(matrix)

    # Step 2 - Terapkan bobot
    weighted = norm_matrix * weights

    # Step 3 - Ideal positif dan negatif
    ideal_best  = np.where(benefit_criteria, weighted.max(axis=0), weighted.min(axis=0))
    ideal_worst = np.where(benefit_criteria, weighted.min(axis=0), weighted.max(axis=0))

    # Step 4 - Hitung jarak Euclidean
    D_plus  = np.linalg.norm(weighted - ideal_best,  axis=1)
    D_minus = np.linalg.norm(weighted - ideal_worst, axis=1)

    # Step 5 - Skor preferensi
    scores = D_minus / (D_plus + D_minus)
    return scores, D_plus, D_minus

# ----------------------------------------------------------
# DATA HOTEL
# Kriteria: Harga (Rp), Fasilitas (1-10), Jarak km, Ulasan (1-10)
# ----------------------------------------------------------
hotel_names = ["Hotel Mutiara", "Hotel Grand", "Hotel Bintang"]

# Baris = hotel, Kolom = [Harga(rb), Fasilitas, Jarak(km), Ulasan]
matrix = np.array([
    [100, 8, 5, 9],   # Hotel Mutiara
    [120, 9, 2, 7],   # Hotel Grand
    [ 90, 7, 6, 8],   # Hotel Bintang
])

# Bobot kriteria (total = 1)
weights = np.array([0.3, 0.3, 0.2, 0.2])

# Jenis kriteria: True = benefit (lebih besar lebih baik), False = cost
# Harga = cost (lebih murah lebih baik), Jarak = cost (lebih dekat lebih baik)
benefit_criteria = np.array([False, True, False, True])

kriteria = ["Harga", "Fasilitas", "Jarak ke Kota", "Ulasan Pelanggan"]

scores, D_plus, D_minus = topsis(matrix, weights, benefit_criteria)
ranking = np.argsort(scores)[::-1]

print("=" * 55)
print("  HASIL TOPSIS - REKOMENDASI HOTEL")
print("=" * 55)
print(f"\n{'Hotel':<16} {'D+':<8} {'D-':<8} {'Skor':<8} {'Rank'}")
print("-" * 55)
for i in ranking:
    rank = list(ranking).index(i) + 1
    print(f"  {hotel_names[i]:<14} {D_plus[i]:.4f}   {D_minus[i]:.4f}   {scores[i]:.4f}   #{rank}")

print(f"\n→ Rekomendasi: {hotel_names[ranking[0]]} adalah hotel terbaik!")
print("\nCatatan:")
print("  - D+ = jarak ke solusi ideal positif (kecil = lebih baik)")
print("  - D- = jarak ke solusi ideal negatif (besar = lebih baik)")
print("  - Skor mendekati 1 = alternatif terbaik")