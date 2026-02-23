"""
Load mini-spectrometer data for shot 51111 and print a wavelength table.

Requirements:
- Use golem_data_loader
- Discard signals (spectra) immediately
- Keep wavelengths from 350 nm to 1100 nm
"""

from __future__ import annotations

from typing import List

import numpy as np
import pandas as pd

from golem_data_loader import GolemDataLoader


def filter_wavelengths_nm(wavelengths_nm: np.ndarray) -> np.ndarray:
    """Return wavelengths between 350 and 1100 nm (inclusive)."""
    mask = (wavelengths_nm >= 350.0) & (wavelengths_nm <= 1100.0)
    return wavelengths_nm[mask]


def build_table(wavelengths_nm: np.ndarray) -> pd.DataFrame:
    """Build a simple table with index and wavelength values."""
    return pd.DataFrame(
        {
            "index": np.arange(len(wavelengths_nm), dtype=int),
            "wavelength_nm": wavelengths_nm,
        }
    )


def main() -> None:
    loader = GolemDataLoader(shot_number=51111)
    minispec = loader.load_minispectrometer_h5()

    # Discard spectra immediately to avoid holding signals in memory.
    spectra_shape = minispec.spectra.shape
    del minispec.spectra

    filtered_wavelengths = filter_wavelengths_nm(minispec.wavelengths)
    table = build_table(filtered_wavelengths)

    print(f"Loaded spectra shape (discarded): {spectra_shape}")
    print(f"Filtered wavelength count: {len(filtered_wavelengths)}")
    print("Wavelength table:")
    print(table.to_string(index=False))


if __name__ == "__main__":
    main()
