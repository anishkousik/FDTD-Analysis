import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 1. Read reflectance data from CSV (with and without MoTe2 layer)
# Assuming the CSV has columns like: Wavelength(um), R_with, R_without
data = pd.read_csv("/Users/anishkousik/Desktop/FDTD Analysis/Material Definintion/Reflectivity/new_data.csv")  # replace with actual filename/path if needed
wavelength_um = data.iloc[:, 0].values            # first column: wavelength in microns
R_with = data.iloc[:, 1].values                   # second column: reflectance with MoTe2
R_without = data.iloc[:, 2].values                # third column: reflectance of bare substrate

# 2. Compute reflectance contrast ΔR/R for each wavelength
deltaR_over_R = (R_with - R_without) / R_without  # ΔR/R = (R_with - R_without) / R_without

# 3. Convert wavelength to photon energy in eV
wavelength_nm = wavelength_um * 1000.0              # convert microns to nanometers
energy_eV = 1240.0 / wavelength_nm                  # E(eV) = 1240 / λ(nm)

# It’s helpful to sort by energy for plotting (ascending energy)
# The data currently might be in increasing wavelength (decreasing energy)
sorted_indices = np.argsort(energy_eV)              # indices to sort energies ascending
energy_eV = energy_eV[sorted_indices]
deltaR_over_R = deltaR_over_R[sorted_indices]

# 4. Plot reflectance contrast vs photon energy
plt.figure(figsize=(6,4))
plt.plot(energy_eV, deltaR_over_R, color='black', linewidth=1.5)
plt.axhline(0, color='gray', linestyle='--', linewidth=0.8)  # horizontal line at ΔR/R = 0 for reference
plt.xlabel("Photon Energy (eV)")
plt.ylabel("Reflectance Contrast ΔR/R")
plt.title("MoTe$_2$ Reflectance Contrast (ΔR/R) vs Photon Energy")
plt.tight_layout()
plt.show()
