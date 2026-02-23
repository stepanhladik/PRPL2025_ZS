"""
Load and display raw camera data from GOLEM using golem_data_loader.

Usage:
    python load_camera_raw_demo.py
"""

import numpy as np
from golem_data_loader import GolemDataLoader


def load_and_show_raw_camera_data(shot_number: int = 50377):
    """
    Load raw fast camera data for a given shot and display sample information.
    
    Args:
        shot_number: The GOLEM shot number (default: 50377)
    """
    print(f"\nLoading raw camera data for shot {shot_number}...")
    print("=" * 70)
    
    # Initialize the loader
    loader = GolemDataLoader(shot_number=shot_number)
    
    # Load fast camera data
    print("\nLoading fast cameras...")
    try:
        cameras = loader.load_fast_cameras()
        
        if not cameras:
            print("No camera data available for this shot.")
            return
        
        print(f"\n✓ Successfully loaded {len(cameras)} camera(s)\n")
        
        # Display information for each camera
        for camera_name, camera_data in cameras.items():
            print("-" * 70)
            print(f"Camera: {camera_name.upper()}")
            print("-" * 70)
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
                print(f"  Shape: {frame.shape}")
                print(f"  Min value: {frame.min()}")
                print(f"  Max value: {frame.max()}")
                print(f"  Mean value: {frame.mean():.2f}")
                print(f"  First 10 pixels: {frame.flatten()[:10]}")
            
            # Show statistics across all frames
            print(f"\n--- Statistics Across All Frames ---")
            all_pixels = camera_data.frames.flatten()
            print(f"Total pixels:      {len(all_pixels):,}")
            print(f"Global min:        {all_pixels.min()}")
            print(f"Global max:        {all_pixels.max()}")
            print(f"Global mean:       {all_pixels.mean():.2f}")
            print(f"Global std dev:    {all_pixels.std():.2f}")
            
            # Show frame-by-frame intensity evolution
            print(f"\n--- Frame-by-Frame Mean Intensity ---")
            frame_means = camera_data.frames.mean(axis=(1, 2)) if camera_data.frames.ndim == 3 else camera_data.frames.mean(axis=1)
            print(f"First 10 frames mean intensity:")
            for i in range(min(10, len(frame_means))):
                print(f"  Frame {i:3d} (t={camera_data.time[i]*1000:7.4f} ms): {frame_means[i]:7.2f}")
            
            if len(frame_means) > 10:
                print(f"  ...")
                print(f"  Frame {len(frame_means)-1:3d} (t={camera_data.time[-1]*1000:7.4f} ms): {frame_means[-1]:7.2f}")
            
    except Exception as e:
        print(f"\n✗ Error loading camera data: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    import sys
    
    # Allow shot number as command line argument
    shot_number = int(sys.argv[1]) if len(sys.argv) > 1 else 50377
    
    load_and_show_raw_camera_data(shot_number)
