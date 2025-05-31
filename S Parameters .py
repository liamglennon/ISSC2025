# Install required libraries
!pip install scikit-rf matplotlib numpy

# Import libraries
import skrf as rf
import matplotlib.pyplot as plt
import numpy as np
from google.colab import files
import os

# === SETTINGS ===
plt.style.use('default')  # start clean
plt.rcParams.update({
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'lines.linewidth': 1.5,
    'axes.grid': True,
    'grid.linestyle': '--',
    'grid.linewidth': 0.5,
    'axes.spines.top': True,
    'axes.spines.right': True,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 9,
    'legend.frameon': False,
    'font.family': 'sans-serif',
    'font.sans-serif': ['DejaVu Sans'],
})

# Output directory
output_dir = "s_parameters_plots"
os.makedirs(output_dir, exist_ok=True)

# Define db() function manually since scikit-rf removed direct access
def db(x):
    return 20 * np.log10(np.abs(x))

# Upload your files
uploaded = files.upload()

# Prepare to store all networks for combined plot
all_networks = {}

# Process each uploaded file
for filename in uploaded.keys():
    # Load the network file
    ntw = rf.Network(filename)

    # Store in dictionary for combined plot later
    all_networks[filename] = ntw

    # Individual plot
    plt.figure(figsize=(6, 4))
    for s_idx in range(ntw.s.shape[1]):  # number of ports
        for s_jdx in range(ntw.s.shape[2]):
            label = f"S{s_idx+1}{s_jdx+1}"
            plt.plot(ntw.f / 1e9, db(ntw.s[:, s_idx, s_jdx]), label=label)

    plt.title(f'S-Parameters: {filename}')
    plt.xlabel('Frequency (GHz)')
    plt.ylabel('Magnitude (dB)')
    plt.legend(loc='best', fontsize=8)
    plt.grid(True, linestyle='--', linewidth=0.5)
    plt.tight_layout()

    # Export PNG + PDF
    base_name = os.path.splitext(filename)[0]
    plt.savefig(os.path.join(output_dir, f"{base_name}_Sparameters.png"), dpi=300)
    plt.savefig(os.path.join(output_dir, f"{base_name}_Sparameters.pdf"))
    plt.close()
    print(f" Saved individual plots for: {filename}")

# Combined plot
plt.figure(figsize=(8, 5))
for filename, ntw in all_networks.items():
    for s_idx in range(ntw.s.shape[1]):  # number of ports
        for s_jdx in range(ntw.s.shape[2]):
            label = f"{os.path.splitext(filename)[0]} S{s_idx+1}{s_jdx+1}"
            plt.plot(ntw.f / 1e9, db(ntw.s[:, s_idx, s_jdx]), label=label)

plt.title('MOLEX Combined S-Parameters')
plt.xlabel('Frequency (GHz)')
plt.ylabel('Magnitude (dB)')
plt.legend(loc='best', fontsize=8)
plt.grid(True, linestyle='--', linewidth=0.5)
plt.tight_layout()

# Export combined PNG + PDF
plt.savefig(os.path.join(output_dir, "Molex_combined_Sparameters.png"), dpi=300)
plt.savefig(os.path.join(output_dir, "Molex_combined_Sparameters.pdf"))
plt.close()
print(" Saved combined S-parameter plot")