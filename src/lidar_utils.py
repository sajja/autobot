"""Utility functions for displaying LIDAR data."""

from typing import List
from src.sensors import LidarReading


def print_lidar_scan(scan_data: List[LidarReading], show_all: bool = False) -> None:
    """
    Print LIDAR scan data in a formatted table.
    
    Args:
        scan_data: List of LidarReading objects
        show_all: If True, show all readings; if False, show sample (default: False)
    """
    print(f"\nLIDAR Scan Results (Total: {len(scan_data)} readings)")
    print("-" * 60)
    print(f"{'Angle (°)':>12} {'Distance (m)':>15} {'Intensity':>15}")
    print("-" * 60)
    
    if show_all:
        # Show all readings
        for reading in scan_data:
            print(f"{reading.angle:>12.0f} {reading.distance:>15.2f} {reading.intensity:>15}")
    else:
        # Show first 10, middle 5, and last 10
        show_indices = list(range(10)) + list(range(175, 180)) + list(range(350, 360))
        
        for i in show_indices:
            if i < len(scan_data):
                reading = scan_data[i]
                print(f"{reading.angle:>12.0f} {reading.distance:>15.2f} {reading.intensity:>15}")
                if i == 9:
                    print("..." + " " * 53 + "...")
                elif i == 179:
                    print("..." + " " * 53 + "...")
    
    print("-" * 60)
    if scan_data:
        print(f"Scan timestamp: {scan_data[0].timestamp:.2f}")
    print()


def save_lidar_scan_csv(scan_data: List[LidarReading], filename: str) -> None:
    """
    Save LIDAR scan data to a CSV file.
    
    Args:
        scan_data: List of LidarReading objects
        filename: Output CSV filename
    """
    with open(filename, 'w') as f:
        f.write("Angle,Distance,Intensity,Timestamp\n")
        for reading in scan_data:
            f.write(f"{reading.angle:.1f},{reading.distance:.3f},{reading.intensity},{reading.timestamp:.6f}\n")
    
    print(f"LIDAR scan saved to {filename}")
