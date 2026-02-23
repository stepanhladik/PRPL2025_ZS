"""
DET100A2 Responsivity mapped to wavelengths from GOLEM shot 51111
Interpolates DET100A2 responsivity data to the exact wavelengths used in shot 51111
"""

import numpy as np
from scipy.interpolate import interp1d
from golem_data_loader import GolemDataLoader
import matplotlib.pyplot as plt

# Load wavelengths from shot 51111
print("Loading wavelengths from GOLEM shot 51111...")
loader = GolemDataLoader(shot_number=51111)
mini_data = loader.load_minispectrometer_h5(h5_filename="IRVISUV_0.h5")

shot_wavelengths = mini_data.wavelengths
print(f"✓ Loaded {len(shot_wavelengths)} wavelengths from shot 51111")
print(f"  Range: {shot_wavelengths[0]:.6f} - {shot_wavelengths[-1]:.6f} nm\n")

# DET100A2 Original calibration data
det_wavelengths_original = np.array([
    320, 330, 340, 350, 360, 370, 380, 390, 400, 420, 440, 460, 480, 500, 520,
    540, 560, 580, 600, 620, 640, 660, 680, 700, 720, 740, 760, 780, 800, 820,
    840, 860, 880, 900, 920, 940, 960, 980, 1000, 1020, 1040, 1060, 1080, 1100
], dtype=float)

det_responsivity_original = np.array([
    0.174, 0.181, 0.184, 0.181, 0.175, 0.17, 0.175, 0.186, 0.193, 0.212, 0.23,
    0.248, 0.269, 0.289, 0.309, 0.332, 0.355, 0.377, 0.399, 0.424, 0.448, 0.468,
    0.488, 0.509, 0.529, 0.548, 0.566, 0.585, 0.601, 0.616, 0.636, 0.651, 0.667,
    0.678, 0.696, 0.711, 0.721, 0.726, 0.708, 0.653, 0.553, 0.415, 0.295, 0.2
], dtype=float)

# Create cubic spline interpolator
interpolator = interp1d(det_wavelengths_original, det_responsivity_original, 
                        kind='cubic', fill_value='extrapolate')

# Interpolate DET100A2 responsivity to shot 51111 wavelengths
print("Interpolating DET100A2 responsivity to shot 51111 wavelengths...")
det_responsivity_interpolated = interpolator(shot_wavelengths)

print(f"✓ Interpolated responsivity data")
print(f"  Responsivity range: {det_responsivity_interpolated.min():.6f} - {det_responsivity_interpolated.max():.6f} A/W\n")

# Save to file
output_file = "DET100A2_responsivity_shot_51111.txt"
print(f"Saving to {output_file}...")

with open(output_file, 'w') as f:
    f.write("DET100A2 Responsivity mapped to GOLEM Shot 51111 Wavelengths\n")
    f.write(f"Mini Spectrometer wavelengths from shot 51111 (2047 points)\n")
    f.write(f"Wavelength range: {shot_wavelengths[0]:.6f} - {shot_wavelengths[-1]:.6f} nm\n")
    f.write("Responsivity interpolated using cubic spline from DET100A2 calibration data\n")
    f.write("="*80 + "\n\n")
    f.write(f"{'Index':<8} {'Wavelength (nm)':<25} {'Responsivity (A/W)':<25}\n")
    f.write("-"*80 + "\n")
    
    for i, (wl, resp) in enumerate(zip(shot_wavelengths, det_responsivity_interpolated)):
        f.write(f"{i:<8d} {wl:<25.10f} {resp:<25.10f}\n")

print(f"✓ Saved to {output_file} ({len(shot_wavelengths)} data points)\n")

# Also print first and last few entries
print(f"{'='*80}")
print("SAMPLE DATA - First 10 entries:")
print(f"{'='*80}")
print(f"{'Index':<8} {'Wavelength (nm)':<25} {'Responsivity (A/W)':<25}")
print("-"*80)
for i in range(10):
    print(f"{i:<8d} {shot_wavelengths[i]:<25.10f} {det_responsivity_interpolated[i]:<25.10f}")

print(f"\n{'='*80}")
print("SAMPLE DATA - Last 10 entries:")
print(f"{'='*80}")
print(f"{'Index':<8} {'Wavelength (nm)':<25} {'Responsivity (A/W)':<25}")
print("-"*80)
for i in range(len(shot_wavelengths)-10, len(shot_wavelengths)):
    print(f"{i:<8d} {shot_wavelengths[i]:<25.10f} {det_responsivity_interpolated[i]:<25.10f}")

# Plot interpolated responsivity with original calibration dots overlaid
print(f"\n{'='*80}")
print("Plotting DET100A2 responsivity with original calibration points...")
print(f"{'='*80}\n")

plt.figure(figsize=(12, 6))
plt.plot(shot_wavelengths, det_responsivity_interpolated, '-', linewidth=2, label='Interpolated (Shot 51111 Wavelengths)')
plt.plot(det_wavelengths_original, det_responsivity_original, 'o', markersize=6, label='Original Calibration Points')
plt.xlabel('Wavelength (nm)', fontsize=12)
plt.ylabel('Responsivity (A/W)', fontsize=12)
plt.title('DET100A2 Detector Responsivity', fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=11)
plt.tight_layout()
plt.show()
