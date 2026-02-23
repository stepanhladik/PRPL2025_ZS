"""
Extract wavelengths from GOLEM shot 51111 mini-spectrometer data
"""

import numpy as np
from golem_data_loader import GolemDataLoader

# Load data from shot 51111
shot_number = 51111
print(f"\nLoading mini-spectrometer data from shot {shot_number}...")

try:
    loader = GolemDataLoader(shot_number=shot_number)
    mini_data = loader.load_minispectrometer_h5(h5_filename="IRVISUV_0.h5")
    
    if mini_data is None:
        print("✗ No mini spectrometer data available for this shot")
    else:
        wavelengths = mini_data.wavelengths
        spectra = mini_data.spectra
        
        print(f"\n✓ Successfully loaded mini-spectrometer data")
        print(f"  Spectra shape: {spectra.shape} (time samples x wavelengths)")
        print(f"  Number of wavelengths: {len(wavelengths)}")
        print(f"  Wavelength range: {wavelengths[0]:.6f} - {wavelengths[-1]:.6f} nm")
        
        # Extract first time fragment
        first_fragment_wavelengths = wavelengths
        
        print(f"\n{'='*70}")
        print(f"WAVELENGTHS FROM FIRST TIME FRAGMENT (Shot {shot_number})")
        print(f"{'='*70}")
        print(f"Total wavelength points: {len(first_fragment_wavelengths)}\n")
        
        # Print wavelengths in a formatted table
        for i, wl in enumerate(first_fragment_wavelengths):
            if i % 10 == 0:  # Print 10 per line for readability
                if i > 0:
                    print()
                print(f"Index {i:4d}-{min(i+9, len(first_fragment_wavelengths)-1):4d}:")
            print(f"  {wl:.6f} nm", end="")
        print("\n")
        
        # Also save to a text file for reference
        output_file = "wavelengths_shot_51111.txt"
        with open(output_file, 'w') as f:
            f.write(f"Wavelengths from GOLEM Shot {shot_number} - Mini Spectrometer\n")
            f.write(f"Total points: {len(first_fragment_wavelengths)}\n")
            f.write(f"Range: {first_fragment_wavelengths[0]:.6f} - {first_fragment_wavelengths[-1]:.6f} nm\n")
            f.write("="*70 + "\n\n")
            for i, wl in enumerate(first_fragment_wavelengths):
                f.write(f"{i:5d}  {wl:.10f}\n")
        
        print(f"✓ Wavelengths saved to {output_file}")
        
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
