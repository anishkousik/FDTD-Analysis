import h5py
import numpy as np
import pandas as pd
import os
import re
from glob import glob

# Directory containing MATLAB files
matlab_files_dir = "/Users/anishkousik/Desktop/FDTD Analysis/W_T Simulation Sweeps/Research comparison/1550"
matlab_files = glob(os.path.join(matlab_files_dir, "*.mat"))

# Function to extract width and thickness from filename
def extract_dimensions_final(filename):
    name = os.path.splitext(filename)[0]
    match = re.search(r'([0-9.]+e?-?[0-9]*)[ _]([0-9.]+e?-?[0-9]*)', name)
    if match:
        return float(match.group(1)), float(match.group(2))
    return None, None

# Function to compute 2D confinement factor
def compute_confinement_factor_2d(file_path, design_width, design_thickness):
    with h5py.File(file_path, 'r') as f:
        y_coords = np.array(f['E_data']['y']).flatten()
        z_coords = np.array(f['E_data']['z']).flatten()

        E = f['E_data']['E']
        Ex = E[0]['real'] + 1j * E[0]['imag']
        Ey = E[1]['real'] + 1j * E[1]['imag']
        Ez = E[2]['real'] + 1j * E[2]['imag']

        E_mag_sq = np.abs(Ex)**2 + np.abs(Ey)**2 + np.abs(Ez)**2

        Ny, Nz = len(y_coords), len(z_coords)
        E_mag_sq_2d = E_mag_sq.reshape((Ny, Nz))

        # Core region: Y centered at 0, Z starts at 0 and ends at design_thickness
        y_core_min = -design_width / 2
        y_core_max = design_width / 2
        z_core_min = 0
        z_core_max = design_thickness

        y_core_idx = np.where((y_coords >= y_core_min) & (y_coords <= y_core_max))[0]
        z_core_idx = np.where((z_coords >= z_core_min) & (z_coords <= z_core_max))[0]

        if len(y_core_idx) == 0 or len(z_core_idx) == 0:
            return 0.0

        # Extract core energy
        core_energy = np.sum(E_mag_sq_2d[np.ix_(y_core_idx, z_core_idx)])
        total_energy = np.sum(E_mag_sq_2d)

        return core_energy / total_energy

# Process all files
results = []
for file_path in matlab_files:
    filename = os.path.basename(file_path)
    width, thickness = extract_dimensions_final(filename)

    if width is None or thickness is None:
        continue

    try:
        conf_2d = compute_confinement_factor_2d(file_path, width, thickness)
        results.append({
            "File": filename,
            "Width (m)": width,
            "Thickness (m)": thickness,
            "Confinement Factor (2D)": conf_2d
        })
    except Exception as e:
        results.append({
            "File": filename,
            "Width (m)": width,
            "Thickness (m)": thickness,
            "Confinement Factor (2D)": f"Error: {e}"
        })

# Create dataframe
df_2d = pd.DataFrame(results)

print(df_2d.to_string(index=False))

# Save to CSV
df_2d.to_csv(os.path.join(matlab_files_dir, "2D_mode_confinement_sweep_6.csv"), index=False)