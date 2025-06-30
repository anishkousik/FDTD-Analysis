import numpy as np

# Constants
c0 = 2.99792458e8          # Speed of light (m/s)
epsilon0 = 8.854187817e-12  # Vacuum permittivity (F/m)
d = 0.7e-9                  # Monolayer thickness (m)

# Validation function for single wavelength
def calculate_sigma(lam_um, n, k):
    """
    Calculate surface conductivity for a single wavelength.
    Returns: (Re_sigma, Im_sigma) in Siemens
    """
    lam_m = lam_um * 1e-6   # Convert µm to meters
    omega = 2 * np.pi * c0 / lam_m  # Angular frequency (rad/s)
    
    # Complex permittivity
    eps1 = n**2 - k**2       # Real part
    eps2 = 2 * n * k         # Imaginary part
    
    # Surface conductivity
    Re_sigma = omega * epsilon0 * eps2 * d
    Im_sigma = omega * epsilon0 * (1 - eps1) * d
    
    return Re_sigma, Im_sigma

# Test cases from literature/dataset
test_points = [
    # (wavelength (µm), n, k, expected Re(σ), expected Im(σ))
    (0.600, 4.37, 1.90, 3.2e-4, -2.8e-4),   # Visible range (high absorption)
    (1.550, 4.84, 0.00, 0.0, -1.7e-4),      # Telecom range (low absorption)
    (1.100, 4.80, 0.25, 1.1e-5, -1.8e-4)    # Near band edge
]

print("Validation Results:")
print("=" * 65)
print(f"{'Wavelength (µm)':>12} | {'n':>6} | {'k':>6} | {'Re(σ) [S]':>12} | {'Im(σ) [S]':>12} | {'Status':<10}")
print("-" * 65)

for lam, n_val, k_val, exp_re, exp_im in test_points:
    # Calculate from function
    calc_re, calc_im = calculate_sigma(lam, n_val, k_val)
    
    # Compare with expected values (10% tolerance)
    tol = 0.1
    re_match = abs(calc_re - exp_re) / exp_re < tol if exp_re != 0 else calc_re == 0
    im_match = abs(calc_im - exp_im) / abs(exp_im) < tol
    
    status = "PASS" if re_match and im_match else "FAIL"
    
    print(f"{lam:12.4f} | {n_val:6.2f} | {k_val:6.2f} | {calc_re:12.2e} | {calc_im:12.2e} | {status:>10}")

# Additional check: Full dataset consistency
print("\nDataset Consistency Check:")
data = np.loadtxt('/Users/anishkousik/Desktop/FDTD Analysis/Reflectivity/MoTe2_multi_Munkhbat.csv', delimiter=',', skiprows=1)
lam_um = data[:, 0]
n_vals = data[:, 1]
k_vals = data[:, 2]

# Calculate σ for entire dataset
omega = 2 * np.pi * c0 / (lam_um * 1e-6)
eps1 = n_vals**2 - k_vals**2
eps2 = 2 * n_vals * k_vals
Re_sigma = omega * epsilon0 * eps2 * d
Im_sigma = omega * epsilon0 * (1 - eps1) * d

# Check for NaN/Inf
assert not np.isnan(Re_sigma).any(), "NaN values in Re(σ)"
assert not np.isnan(Im_sigma).any(), "NaN values in Im(σ)"
assert np.isfinite(Re_sigma).all(), "Non-finite values in Re(σ)"
assert np.isfinite(Im_sigma).all(), "Non-finite values in Im(σ)"

# Verify physical constraints
assert (Re_sigma >= 0).all(), "Negative Re(σ) found"
assert (eps2 >= 0).all(), "Negative extinction (k) detected"

print("All checks passed: No NaN/Inf values, Re(σ) physically valid")