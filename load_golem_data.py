"""
Load GOLEM raw data for a specific shot number.

Usage:
    python load_golem_data.py 50377
"""

import sys
from golem_data_loader import GolemDataLoader


def load_shot_data(shot_number: int):
    """
    Load fast spectrometry and fast camera data for a given shot.
    
    Args:
        shot_number: The GOLEM shot number
        
    Returns:
        Tuple of (spectrometry_data, fast_camera_data)
    """
    loader = GolemDataLoader(shot_number=shot_number)
    
    print(f"\nLoading data for shot {shot_number}...")
    print("-" * 50)
    
    # Load fast spectrometry data
    print("Loading fast spectrometry data...")
    spectrometry_data = loader.load_fast_spectrometry()
    
    print(f"Loaded {len(spectrometry_data)} spectrometry signals:")
    for name, signal in spectrometry_data.items():
        print(f"  - {name}: {len(signal.time)} data points, time range: {signal.time[0]:.4f}s - {signal.time[-1]:.4f}s")
    
    # Load fast camera data
    print("\nLoading fast camera data...")
    try:
        fast_cameras = loader.load_fast_cameras()
        
        print(f"Loaded {len(fast_cameras)} camera(s):")
        for camera_name, camera_data in fast_cameras.items():
            print(f"  - {camera_name}: {camera_data.frames.shape} frames, dtype: {camera_data.frames.dtype}")
    except Exception as e:
        print(f"  Warning: Could not load fast cameras: {e}")
        fast_cameras = None
    
    print("-" * 50)
    return spectrometry_data, fast_cameras


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python load_golem_data.py <shot_number>")
        print("Example: python load_golem_data.py 50377")
        sys.exit(1)
    
    try:
        shot_number = int(sys.argv[1])
    except ValueError:
        print(f"Error: '{sys.argv[1]}' is not a valid shot number (must be an integer)")
        sys.exit(1)
    
    spectrometry_data, fast_cameras = load_shot_data(shot_number)
