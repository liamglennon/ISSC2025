# Install dependencies
!pip install numpy pandas plotly kaleido

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from google.colab import files
import os

# === CONFIGURATION ===
radial_range = [-80, -50]
export_dir = 'exports'

# Prepare output directories (only for combined PDF and PNG exports)
for subdir in ['pdf', 'png']:
    os.makedirs(os.path.join(export_dir, subdir), exist_ok=True)

# Upload CSV files
uploaded = files.upload()

# Constants
P_t_dBm = 20
G_r_dBi = 11.59
cable_loss_dB = -7.2
freq_Hz = 5.9e9
distance_m = 5.88
c = 3e8
wavelength = c / freq_Hz
path_loss = 20 * np.log10(4 * np.pi * distance_m / wavelength)

# Storage for results and combined plot data
results = []
combined_datasets = []

# Helpers
def clean_filename(filename):
    return filename.replace(' ', '_').replace('(', '').replace(')', '').replace('.csv', '')

def rotate_angles(angles, rotation_deg):
    return (angles + rotation_deg) % 360

def apply_styling(fig):
    fig.update_layout(
        font=dict(family="Arial", size=12, color="black"),
        title=dict(x=0.5, xanchor='center', font=dict(size=14, family='Arial', color='black')),
        polar=dict(
            radialaxis=dict(range=radial_range, dtick=5, gridcolor='gray', gridwidth=0.5,
                            linecolor='black', linewidth=1, tickfont=dict(size=10, family='Arial')),
            angularaxis=dict(direction='clockwise', rotation=90, gridcolor='gray', gridwidth=0.5,
                             linecolor='black', linewidth=1, tickfont=dict(size=10, family='Arial'))
        ),
        showlegend=True,
        legend=dict(font=dict(size=10, family='Arial'),
                    bordercolor='black', borderwidth=0.5,
                    x=1.05, y=1),
        template='none',
        paper_bgcolor='white',
        plot_bgcolor='white'
    )
    return fig

def export_figure(fig, filename_base):
    pdf_path = os.path.join(export_dir, 'pdf', f'{filename_base}.pdf')
    png_path = os.path.join(export_dir, 'png', f'{filename_base}.png')
    fig.write_image(pdf_path, engine='kaleido')
    fig.write_image(png_path, engine='kaleido')

# Process each uploaded CSV file
colors = ['blue', 'green', 'orange', 'red', 'purple', 'brown', 'magenta', 'cyan']
for idx, filename in enumerate(uploaded.keys()):
    # Read data from CSV
    df = pd.read_csv(filename, names=["Angle", "Signal Strength"], skiprows=1)
    angles = df["Angle"].values
    signal = df["Signal Strength"].values

    # Rotate the angles based on the average of the top 10% of signal values
    threshold = np.percentile(signal, 90)
    best_mask = signal >= threshold
    best_angles = angles[best_mask]
    central_angle = np.mean(best_angles) if len(best_angles) > 0 else 0
    snapped_rotation = round(central_angle / 90) * 90

    rotated_angles = rotate_angles(angles, -snapped_rotation)
    sort_idx = np.argsort(rotated_angles)
    rotated_angles = rotated_angles[sort_idx]
    signal = signal[sort_idx]

    # Determine peak power and its corresponding angle
    peak_power = np.max(signal)
    peak_angle = rotated_angles[np.argmax(signal)]

    filename_base = clean_filename(filename)

    # Create individual polar plot for this dataset
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=signal,
        theta=rotated_angles,
        mode='lines',
        line=dict(color=colors[idx % len(colors)], width=1),
        name='Signal'
    ))
    fig.add_trace(go.Scatterpolar(
        r=[peak_power],
        theta=[peak_angle],
        mode='markers',
        marker=dict(size=6, color='red', symbol='circle'),
        name='Peak Power'
    ))

    fig = apply_styling(fig)
    fig.update_layout(title_text=f'Polar Plot: {filename_base} (Rotation: {-snapped_rotation}°)')

    # Export individual figure
    export_figure(fig, filename_base)

    # Append results (excluding beamwidth)
    results.append({
        'Filename': filename,
        'Rotation Applied (deg)': -snapped_rotation,
        'Peak Power (dBm)': peak_power,
        'Peak Angle (deg)': peak_angle,
    })

    # Store data for the combined plot
    combined_datasets.append({
        'filename_base': filename_base,
        'rotated_angles': rotated_angles,
        'signal': signal,
        'peak_power': peak_power,
        'peak_angle': peak_angle,
        'color': colors[idx % len(colors)]
    })

# Create a combined polar plot for all datasets
combined_fig = go.Figure()
for dataset in combined_datasets:
    combined_fig.add_trace(go.Scatterpolar(
         r=dataset['signal'],
         theta=dataset['rotated_angles'],
         mode='lines',
         line=dict(color=dataset['color'], width=1),
         name=f"Signal - {dataset['filename_base']}"
    ))
    combined_fig.add_trace(go.Scatterpolar(
         r=[dataset['peak_power']],
         theta=[dataset['peak_angle']],
         mode='markers',
         marker=dict(size=6, color='red', symbol='circle'),
         name=f"Peak - {dataset['filename_base']}"
    ))

combined_fig = apply_styling(combined_fig)
combined_fig.update_layout(title_text='DIY')
export_figure(combined_fig, "combined_plot")

# Export summary CSV
results_df = pd.DataFrame(results)
summary_csv_path = os.path.join(export_dir, 'results_summary.csv')
results_df.to_csv(summary_csv_path, index=False)

print("Export complete! You can download the files manually from the Colab Files panel.")

# Optional: List exported files
for root, dirs, files in os.walk(export_dir):
    level = root.replace(export_dir, '').count(os.sep)
    indent = ' ' * 2 * level
    print(f'{indent}{os.path.basename(root)}/')
    subindent = ' ' * 2 * (level + 1)
    for f in files:
        print(f'{subindent}{f}')