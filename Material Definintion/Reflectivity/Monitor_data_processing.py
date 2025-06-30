import numpy as np
import matplotlib.pyplot as plt

# ——— Load your data from text files, skipping header lines ———
# Each file has two header lines before the data starts
lam, R_with = np.loadtxt("/Users/anishkousik/Desktop/FDTD Analysis/Reflectivity/with_mote2.txt", delimiter=',', skiprows=3, unpack=True)
_,   R_without = np.loadtxt("/Users/anishkousik/Desktop/FDTD Analysis/Reflectivity/without_mote2.txt", delimiter=',', skiprows=3, unpack=True)

deltaR_R = (R_with - R_without) / R_without

# ——— Compute Reflectance Contrast ΔR/R ———
deltaR_R = (R_with - R_without) / R_without

# ——— Convert wavelength (µm) to photon energy (eV) ———
# E[eV] = hc / λ[µm], where hc ≈ 1.23984193 eV·µm
energy = 1.23984193 / lam

# ——— Sort by increasing energy for a proper x-axis ———
idx = np.argsort(energy)
E_sorted       = energy[idx]
deltaR_R_sorted = deltaR_R[idx]

# ——— Plot Reflectance Contrast vs Photon Energy ———
plt.figure(figsize=(6,4))
plt.plot(E_sorted, deltaR_R_sorted, marker='o', linestyle='-')
plt.xlabel('Photon Energy (eV)')
plt.ylabel('Reflectance Contrast ΔR/R')
plt.title('MoTe₂ Reflectance Contrast vs Energy')
plt.grid(True)
plt.tight_layout()
plt.show()