import pandas as pd
import matplotlib.pyplot as plt

# Reload the uploaded files after state reset
conductivity_path = "/Users/anishkousik/Desktop/FDTD Analysis/Material Definintion/Reflectivity/MoTe2_monolayer_conductivity.csv"
reflectivity_path = "/Users/anishkousik/Desktop/FDTD Analysis/Material Definintion/Reflectivity/MoTe2_monolayer_reflectivity.csv"

# Load both CSVs
df_sigma = pd.read_csv(conductivity_path)
df_nk = pd.read_csv(reflectivity_path)

# Extract data
wavelength_cond = df_sigma.iloc[:, 0].values  # in um
re_sigma = df_sigma.iloc[:, 1].values
im_sigma = df_sigma.iloc[:, 2].values

wavelength_nk = df_nk.iloc[:, 0].values  # in um
n = df_nk.iloc[:, 1].values
k = df_nk.iloc[:, 2].values

# Convert wavelengths to nm for plotting
wavelength_nm_cond = wavelength_cond * 1000
wavelength_nm_nk = wavelength_nk * 1000

# Plot Refractive Index (n, k)
plt.figure(figsize=(10, 5))
plt.plot(wavelength_nm_nk, n, label='Refractive index (n)')
plt.plot(wavelength_nm_nk, k, label='Extinction coefficient (k)')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Value')
plt.title('MoTe2 Refractive Index and Extinction Coefficient')
plt.xlim(400, 1600)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Plot Conductivity (real and imaginary)
plt.figure(figsize=(10, 5))
plt.plot(wavelength_nm_cond, re_sigma, label='Re[σ]')
plt.plot(wavelength_nm_cond, im_sigma, label='Im[σ]')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Conductivity (S)')
plt.title('MoTe2 Sheet Conductivity')
plt.xlim(400, 1600)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
