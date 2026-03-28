import numpy as np
from sklearn.preprocessing import MinMaxScaler

# ============================================================
# CHALLENGE 2 - TOPSIS untuk Pemilihan Universitas
# Kriteria: Biaya Kuliah, Akreditasi, Lokasi (jarak), Fasilitas
# ============================================================

def topsis(matrix, weights, benefit_criteria):
    scaler      = MinMaxScaler()
    norm_matrix = scaler.fit_transform(matrix)
    weighted    = norm_matrix * weights
    ideal_best  = np.where(benefit_criteria, weighted.max(axis=0), weighted.min(axis=0))
    ideal_worst = np.where(benefit_criteria, weighted.min(axis=0), weighted.max(axis=0))
    D_plus      = np.linalg.norm(weighted - ideal_best,  axis=1)
    D_minus     = np.linalg.norm(weighted - ideal_worst, axis=1)
    return D_minus / (D_plus + D_minus), D_plus, D_minus

universitas = ["Universitas A", "Universitas B", "Universitas C", "Universitas D"]

# Kolom: [Biaya(juta/th), Akreditasi(1-4), Jarak(km), Fasilitas(1-10)]
# Akreditasi: 4=A, 3=B, 2=C, 1=D
matrix = np.array([
    [25,  4, 50, 9],   # Univ A: mahal, akreditasi A, jauh, fasilitas bagus
    [15,  3, 20, 7],   # Univ B: menengah, akreditasi B, dekat, oke
    [10,  2, 10, 5],   # Univ C: murah, akreditasi C, sangat dekat, biasa
    [20,  4, 80, 8],   # Univ D: mahal, akreditasi A, sangat jauh, bagus
])

weights          = np.array([0.30, 0.35, 0.20, 0.15])
# Biaya=cost, Akreditasi=benefit, Jarak=cost, Fasilitas=benefit
benefit_criteria = np.array([False, True, False, True])
kriteria         = ["Biaya", "Akreditasi", "Jarak", "Fasilitas"]

scores, D_plus, D_minus = topsis(matrix, weights, benefit_criteria)
ranking = np.argsort(scores)[::-1]

print("=" * 60)
print("  CHALLENGE 2 - TOPSIS PEMILIHAN UNIVERSITAS")
print("=" * 60)
print(f"\nBobot Kriteria:")
for k, w in zip(kriteria, weights):
    print(f"  {k:<12}: {w:.2f} ({w*100:.0f}%)")

print(f"\n{'Universitas':<16} {'D+':<8} {'D-':<8} {'Skor':<8} Rank")
print("-" * 60)
for i in ranking:
    rank = list(ranking).index(i) + 1
    print(f"  {universitas[i]:<14} {D_plus[i]:.4f}   {D_minus[i]:.4f}   {scores[i]:.4f}   #{rank}")

print(f"\n→ Rekomendasi: {universitas[ranking[0]]}")