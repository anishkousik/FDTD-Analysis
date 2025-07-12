import numpy as np

# Step 1: Load the n,k data from the CSV file (skip header row).
data = np.loadtxt('/Users/anishkousik/Desktop/FDTD Analysis/Reflectivity/MoTe2_multi_Munkhbat.csv', delimiter=',', skiprows=1)
lam_um = data[:, 0]        # Wavelength in micrometers
n = data[:, 1]             # refractive index
k = data[:, 2]             # extinction coefficient

# Step 2: Define constants and monolayer thickness.
c0 = 2.99792458e8          # speed of light in vacuum (m/s)
epsilon0 = 8.854187817e-12 # vacuum permittivity (F/m)
d_monolayer = 0.7e-9       # monolayer thickness ~0.7 nm in meters

# Step 3: Convert wavelength to angular frequency omega = 2πc/λ.
lam_m = lam_um * 1e-6      # convert wavelength to meters
omega = 2 * np.pi * c0 / lam_m  # angular frequency array (rad/s)

# Step 4: Compute complex relative permittivity ε = (n + i k)^2.
eps_complex = (n + 1j*k)**2
eps1 = np.real(eps_complex)   # ε' (real part)
eps2 = np.imag(eps_complex)   # ε'' (imaginary part)