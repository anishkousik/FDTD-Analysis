import h5py
import numpy as np
import pandas as pd
import os
import re
from glob import glob

# Compute confinement factor along Z (thickness)
def compute_confinement_factor_1d_z(file_path, design_thickness):
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

        # Integrate over y-axis to get power profile as a function of z
        power_profile_z = np.sum(E_mag_sq_2d, axis=0)

        # Define core from z = 0 to z = thickness (as per your setup)
        z_core_idx = np.where((z_coords >= 0) & (z_coords <= design_thickness))[0]

        if len(z_core_idx) == 0:
            return 0.0

        core_energy = np.sum(power_profile_z[z_core_idx])
        total_energy = np.sum(power_profile_z)

        return core_energy / total_energy

# Extract dimensions from filename
def extract_dimensions_final(filename):
    name = os.path.splitext(filename)[0]
    match = re.search(r'([0-9.]+e?-?[0-9]*)[ _]([0-9.]+e?-?[0-9]*)', name)
    if match:
        return float(match.group(1)), float(match.group(2))
    return None, None

# Main processing
matlab_files_dir = "./New Monitor Dimensions Sweep_2"
matlab_files = glob(os.path.join(matlab_files_dir, "*.mat"))

results = []

for file_path in matlab_files:
    filename = os.path.basename(file_path)
    width, thickness = extract_dimensions_final(filename)

    if width is None or thickness is None:
        print(f"Skipping {filename}: couldn't extract width/thickness.")
        continue

    try:
        conf_z = compute_confinement_factor_1d_z(file_path, design_thickness=thickness)
        results.append({
            "File": filename,
            "Width (m)": width,
            "Thickness (m)": thickness,
            "Confinement Factor (1D Z)": conf_z
        })
    except Exception as e:
        print(f"Error processing {filename}: {e}")
        results.append({
            "File": filename,
            "Width (m)": width,
            "Thickness (m)": thickness,
            "Confinement Factor (1D Z)": f"Error: {e}"
        })

# Output results
df = pd.DataFrame(results)
print(df.to_string(index=False))

# Save to CSV
df.to_csv(os.path.join(matlab_files_dir, "1D_Z_mode_confinement_sweep_2_new monitor.csv"), index=False)
