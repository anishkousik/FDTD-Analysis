import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FormatStrFormatter

# Load the uploaded CSV file
#file_path = "./ACTUAL CSV DATA/2D_YZ/2D_mode_confinement_sweep_2_new monitor.csv"
file_path = "./ACTUAL CSV DATA/Transmission/Transmission_data_sweep_1.csv"
df = pd.read_csv(file_path)

# Pivot the data to prepare for heatmap plotting
pivot_table = (
    df
    .groupby(['width', 'thickness'])['transmission']
    .max()
    .unstack()
)

# Create meshgrid for plotting
X, Y = np.meshgrid(pivot_table.columns.values, pivot_table.index.values)

# Plotting the heatmap
fig, ax = plt.subplots(figsize=(10, 8))
contour = ax.contourf(
    X * 1e6,              # convert m → μm
    Y * 1e6,
    pivot_table.values,
    levels=100,
    cmap='viridis'
)
cbar = fig.colorbar(contour, ax=ax, label='Transmission')

# attach scientific‐notation formatters
ax.xaxis.set_major_formatter(FormatStrFormatter('%.2e'))
ax.yaxis.set_major_formatter(FormatStrFormatter('%.2e'))

# rotate x‐labels so they don’t overlap
plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

ax.set_xlabel('Width (µm)')
ax.set_ylabel('Thickness (µm)')
ax.set_title('Transmission Heatmap (Width vs Thickness)')
plt.tight_layout()
plt.show()
