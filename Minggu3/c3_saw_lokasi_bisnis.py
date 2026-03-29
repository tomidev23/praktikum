import numpy as np

# ============================================================
# CHALLENGE 3 - SAW (Simple Additive Weighting)
# untuk Penentuan Lokasi Bisnis Terbaik
# Kriteria: Biaya Sewa, Akses Pelanggan, Tingkat Persaingan
# ============================================================

def saw(matrix, weights, benefit_criteria):
    """
    SAW - Simple Additive Weighting.

    Langkah:
    1. Normalisasi matriks:
       - Benefit: nilai / max(nilai per kolom)
       - Cost   : min(nilai per kolom) / nilai
    2. Kalikan dengan bobot
    3. Jumlahkan → skor preferensi
    """
    m, n = matrix.shape
    norm_matrix = np.zeros((m, n))

    for j in range(n):
        col = matrix[:, j]
        if benefit_criteria[j]:
            norm_matrix[:, j] = col / col.max()   # Benefit
        else:
            norm_matrix[:, j] = col.min() / col   # Cost

    weighted_scores = norm_matrix * weights
    return weighted_scores.sum(axis=1), norm_matrix

lokasi    = ["Lokasi A (Pusat Kota)", "Lokasi B (Mall)", "Lokasi C (Pinggiran)"]
kriteria  = ["Biaya Sewa", "Akses Pelanggan", "Tingkat Persaingan"]

# Kolom: [Biaya sewa (juta/bln), Akses pelanggan (1-10), Persaingan (1-10)]
# Persaingan rendah = lebih baik 
matrix = np.array([
    [15.0, 9, 8],   # Lokasi A: mahal, ramai, persaingan tinggi
    [12.0, 8, 7],   # Lokasi B: menengah, cukup ramai
    [ 5.0, 5, 3],   # Lokasi C: murah, sepi, persaingan rendah
], dtype=float)

weights          = np.array([0.40, 0.35, 0.25])
benefit_criteria = np.array([False, True, False])  # Sewa=cost, Akses=benefit, Saingan=cost

scores, norm_matrix = saw(matrix, weights, benefit_criteria)
ranking = np.argsort(scores)[::-1]

print("=" * 60)
print("  CHALLENGE 3 - SAW PEMILIHAN LOKASI BISNIS")
print("=" * 60)

print("\nMatriks Normalisasi:")
header = f"  {'Lokasi':<24}" + "".join(f"{k:<20}" for k in kriteria) + "Skor"
print(header)
print("-" * 80)
for i in range(len(lokasi)):
    row = f"  {lokasi[i]:<24}"
    for j in range(len(kriteria)):
        row += f"{norm_matrix[i,j]:.4f}              "[:20]
    row += f"{scores[i]:.4f}"
    print(row)

print("\nRanking Akhir:")
for rank, i in enumerate(ranking, 1):
    print(f"  #{rank} {lokasi[i]:<26}: skor {scores[i]:.4f}")

print(f"\n→ Rekomendasi: {lokasi[ranking[0]]} adalah lokasi bisnis terbaik!")
print("\nCatatan SAW:")
print("  - Benefit: normalisasi = nilai / nilai maks")
print("  - Cost   : normalisasi = nilai min / nilai")
print("  - Skor akhir = Σ (bobot × nilai ternormalisasi)")