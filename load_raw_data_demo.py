"""
Load and display raw data from GOLEM using golem_data_loader.

This script demonstrates loading raw spectrometry and camera data
based on shot number.

Usage:
    python load_raw_data_demo.py [shot_number]
    
Example:
    python load_raw_data_demo.py 50377
"""

import numpy as np
from golem_data_loader import GolemDataLoader


def load_and_show_raw_data(shot_number: int = 50377):
    """
    Load raw data for a given shot and display sample information.
    
    Args:
        shot_number: The GOLEM shot number (default: 50377)
    """
    print(f"\n{'='*70}")
    print(f"LOADING RAW DATA FOR SHOT {shot_number}")
    print(f"{'='*70}\n")
    
    # Initialize the loader
    loader = GolemDataLoader(shot_number=shot_number)
    
    # ===== LOAD FAST SPECTROMETRY DATA =====
    print("FAST SPECTROMETRY DATA")
    print("-" * 70)
    try:
        spec_data = loader.load_fast_spectrometry()
        
        print(f"✓ Successfully loaded {len(spec_data)} spectroscopy signals\n")
        
        # Display information for each signal
        for signal_name, signal in spec_data.items():
            print(f"\n{'─'*70}")
            print(f"Signal: {signal.label}")
            print(f"{'─'*70}")
            print(f"Number of samples:  {len(signal.time):,}")
            print(f"Time range:         {signal.time[0]:.6f}s to {signal.time[-1]:.6f}s")
            print(f"Duration:           {(signal.time[-1] - signal.time[0])*1000:.3f} ms")
            print(f"Sampling rate:      ~{1/np.mean(np.diff(signal.time)):.0f} Hz")
            
            # Show sample of raw data
            print(f"\n--- Sample Raw Data (First 10 Points) ---")
            print(f"{'Index':<8} {'Time (ms)':<12} {'Intensity':<12}")
            print("-" * 35)
            for i in range(min(10, len(signal.time))):
                print(f"{i:<8} {signal.time[i]*1000:<12.4f} {signal.intensity[i]:<12.6f}")
            
            # Show statistics
            print(f"\n--- Statistics ---")
            print(f"Intensity min:      {signal.intensity.min():.6f}")
            print(f"Intensity max:      {signal.intensity.max():.6f}")
            print(f"Intensity mean:     {signal.intensity.mean():.6f}")
            print(f"Intensity std dev:  {signal.intensity.std():.6f}")
            
            # Show peak locations
            print(f"\n--- Peak Analysis ---")
            peak_idx = np.argmax(signal.intensity)
            peak_time = signal.time[peak_idx]
            peak_value = signal.intensity[peak_idx]
            print(f"Peak at:            t = {peak_time*1000:.4f} ms")
            print(f"Peak value:         {peak_value:.6f}")
            
            # Show a few points around the peak
            print(f"\n--- Data Around Peak ---")
            start_idx = max(0, peak_idx - 5)
            end_idx = min(len(signal.time), peak_idx + 6)
            print(f"{'Index':<8} {'Time (ms)':<12} {'Intensity':<12} {'Notes'}")
            print("-" * 50)
            for i in range(start_idx, end_idx):
                note = "  <-- PEAK" if i == peak_idx else ""
                print(f"{i:<8} {signal.time[i]*1000:<12.4f} {signal.intensity[i]:<12.6f} {note}")
            
            # Show raw dataframe info
            print(f"\n--- Raw DataFrame Info ---")
            print(f"Shape:              {signal.raw_dataframe.shape}")
            print(f"Columns:            {list(signal.raw_dataframe.columns)}")
            print(f"\nFirst few rows of raw dataframe:")
            print(signal.raw_dataframe.head())
            
    except Exception as e:
        print(f"\n✗ Error loading spectrometry data: {e}")
        import traceback
        traceback.print_exc()
    
    # ===== TRY TO LOAD CAMERA DATA =====
    print(f"\n\n{'='*70}")
    print("FAST CAMERA DATA")
    print("-" * 70)
    try:
        cameras = loader.load_fast_cameras()
        
        print(f"✓ Successfully loaded {len(cameras)} camera(s)\n")
        
        # Display information for each camera
        for camera_name, camera_data in cameras.items():
            print(f"\n{'─'*70}")
            print(f"Camera: {camera_name.upper()}")
            print(f"{'─'*70}")
            print(f"Camera Type:       {camera_data.camera_type}")
            print(f"Frame Rate:        {camera_data.frame_rate:,.0f} fps")
            print(f"Number of Frames:  {camera_data.frames.shape[0]}")
            print(f"Frame Shape:       {camera_data.frames.shape}")
            print(f"Data Type:         {camera_data.frames.dtype}")
            print(f"Time Range:        {camera_data.time[0]:.6f}s to {camera_data.time[-1]:.6f}s")
            print(f"Duration:          {(camera_data.time[-1] - camera_data.time[0])*1000:.3f} ms")
            
            # Show sample of raw data from first few frames
            print(f"\n--- Sample Raw Data (First 3 Frames) ---")
            for i in range(min(3, camera_data.frames.shape[0])):
                frame = camera_data.frames[i]
                print(f"\nFrame {i} (t = {camera_data.time[i]*1000:.4f} ms):")
                print(f"  Shape:       {frame.shape}")
                print(f"  Min value:   {frame.min()}")
                print(f"  Max value:   {frame.max()}")
                print(f"  Mean value:  {frame.mean():.2f}")
                if frame.size <= 20:
                    print(f"  All pixels:  {frame.flatten()}")
                else:
                    print(f"  First 10 pixels: {frame.flatten()[:10]}")
            
    except Exception as e:
        print(f"⚠ Camera data not available for this shot: {e}")
        print(f"  (This is normal - not all shots have camera data)")
    
    print(f"\n{'='*70}\n")


if __name__ == "__main__":
    import sys
    
    # Allow shot number as command line argument
    shot_number = int(sys.argv[1]) if len(sys.argv) > 1 else 50377
    
    load_and_show_raw_data(shot_number)
