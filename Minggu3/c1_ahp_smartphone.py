import numpy as np

# ============================================================
# CHALLENGE 1 - AHP untuk Pemilihan Smartphone
# Kriteria: Kamera, Baterai, Performa, Harga
# ============================================================

def ahp_method(criteria_matrix):
    eigvals, eigvecs = np.linalg.eig(criteria_matrix)
    max_index = np.argmax(eigvals)
    weights = eigvecs[:, max_index]
    return (weights / np.sum(weights)).real

def consistency_ratio(matrix, weights):
    n = len(matrix)
    RI = [0, 0, 0.58, 0.90, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49]
    lambda_max = np.dot(np.dot(matrix, weights), 1 / weights).mean()
    CI = (lambda_max - n) / (n - 1)
    return CI / RI[n - 1]

# Matriks perbandingan kriteria
# Kamera dianggap paling penting untuk smartphone modern
criteria_matrix = np.array([
    [1,   3,   2,   5  ],  # Kamera
    [1/3, 1,   1/2, 3  ],  # Baterai
    [1/2, 2,   1,   4  ],  # Performa
    [1/5, 1/3, 1/4, 1  ],  # Harga
])

kriteria     = ["Kamera", "Baterai", "Performa", "Harga"]
alternatif   = ["Samsung Galaxy S24", "iPhone 15", "Xiaomi 14 Pro"]

weights = ahp_method(criteria_matrix)
CR      = consistency_ratio(criteria_matrix, weights)

# Skor per alternatif per kriteria (0–1, makin tinggi makin baik)
# Untuk Harga: tinggi = lebih murah (lebih menguntungkan)
alt_matrix = np.array([
    # Kamera  Baterai  Performa  Harga
    [0.85,   0.70,    0.80,     0.50],  # Samsung
    [0.90,   0.65,    0.85,     0.40],  # iPhone
    [0.80,   0.80,    0.75,     0.75],  # Xiaomi
])

scores  = alt_matrix @ weights
ranking = np.argsort(scores)[::-1]

print("=" * 55)
print("  CHALLENGE 1 - AHP PEMILIHAN SMARTPHONE")
print("=" * 55)
print(f"\nBobot Kriteria:")
for k, w in zip(kriteria, weights):
    print(f"  {k:<12}: {w:.4f} ({w*100:.1f}%)")
print(f"\n  CR = {CR:.4f}  {'✓ Konsisten' if CR < 0.1 else '✗ Tidak Konsisten'}")

print("\nRanking Smartphone:")
for rank, i in enumerate(ranking, 1):
    print(f"  #{rank} {alternatif[i]:<22}: skor {scores[i]:.4f}")

print(f"\n→ Rekomendasi: {alternatif[ranking[0]]}")