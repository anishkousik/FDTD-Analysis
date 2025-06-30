import pandas as pd
import io

data_string = """
1.05e-006 1.1e-006 0.99816
1.15e-006 1.2e-006 0.998173
1.2e-006 1.25e-006 0.998178
"""

# Use io.StringIO to treat the string as a file
data_io = io.StringIO(data_string)

# Read the data into a pandas DataFrame, specifying space as the delimiter
df = pd.read_csv(data_io, sep='\s+', header=None)

# Assign column names
df.columns = ['width' , 'thickness','transmission']

# Save to CSV
output_filename = "Transmission_data_sweep_6.csv"
df.to_csv(output_filename, index=False)

print(f"Data saved to {output_filename}")