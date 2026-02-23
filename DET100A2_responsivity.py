"""
DET100A2 Responsivity Interpolation
Interpolates detector responsivity data to provide values for each 0.1 nm wavelength step
"""

import numpy as np
from scipy.interpolate import interp1d

# Original calibration data (wavelength in nm, responsivity in A/W)
wavelengths_original = np.array([
    320, 330, 340, 350, 360, 370, 380, 390, 400, 420, 440, 460, 480, 500, 520,
    540, 560, 580, 600, 620, 640, 660, 680, 700, 720, 740, 760, 780, 800, 820,
    840, 860, 880, 900, 920, 940, 960, 980, 1000, 1020, 1040, 1060, 1080, 1100
], dtype=float)

responsivity_original = np.array([
    0.174, 0.181, 0.184, 0.181, 0.175, 0.17, 0.175, 0.186, 0.193, 0.212, 0.23,
    0.248, 0.269, 0.289, 0.309, 0.332, 0.355, 0.377, 0.399, 0.424, 0.448, 0.468,
    0.488, 0.509, 0.529, 0.548, 0.566, 0.585, 0.601, 0.616, 0.636, 0.651, 0.667,
    0.678, 0.696, 0.711, 0.721, 0.726, 0.708, 0.653, 0.553, 0.415, 0.295, 0.2
], dtype=float)

# Create cubic spline interpolator
interpolator = interp1d(wavelengths_original, responsivity_original, kind='cubic', fill_value='extrapolate')

# Generate wavelengths for each 0.1 nm step
wavelengths_interpolated = np.arange(320.0, 1100.1, 0.1)

# Interpolate responsivity values
responsivity_interpolated = interpolator(wavelengths_interpolated)

# Create output data
det100a2_data = {
    'wavelengths': wavelengths_interpolated,
    'responsivity': responsivity_interpolated
}

# Print all interpolated values
print("DET100A2 Responsivity - Interpolated to 0.1 nm resolution")
print("=" * 70)
print(f"{'Wavelength (nm)':<20} {'Responsivity (A/W)':<20}")
print("=" * 70)

for wl, resp in zip(wavelengths_interpolated, responsivity_interpolated):
    print(f"{wl:<20.1f} {resp:<20.6f}")

print("=" * 70)
print(f"Total interpolated points: {len(wavelengths_interpolated)}")
print(f"Wavelength range: {wavelengths_interpolated[0]:.1f} - {wavelengths_interpolated[-1]:.1f} nm")
print(f"Responsivity range: {responsivity_interpolated.min():.6f} - {responsivity_interpolated.max():.6f} A/W")
