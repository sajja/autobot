"""Test LIDAR distance calculations."""

from src.environment import Environment
from src.bot import Bot


def main():
    """Test LIDAR returns correct distances to walls."""
    
    # Create environment (25m x 25m)
    env = Environment(width=25.0, height=25.0, resolution=0.1)
    
    # Create bot with 5m LIDAR range
    bot = Bot(lidar_frequency=1.0)
    
    # Place bot in center
    env.set_bot_position(x=12.5, y=12.5, orientation=0.0)
    
    # Update bot's environment context
    bot.position = (12.5, 12.5)
    bot.environment_bounds = (25.0, 25.0)
    
    # Initialize and scan
    bot.initialize()
    scan_data = bot.get_lidar_scan()
    
    print("\n" + "="*70)
    print("LIDAR Test Results - Distance to Walls")
    print("="*70)
    print(f"Bot Position: (12.5, 12.5)")
    print(f"Environment: 25m x 25m")
    print(f"LIDAR Max Range: {bot.lidar.max_range}m")
    print("="*70)
    print(f"{'Angle':>8} {'Expected Distance':>20} {'Actual Distance':>18} {'Intensity':>12}")
    print("-"*70)
    
    # Test specific angles
    test_angles = [
        (0, 12.5, "Right to wall (x=25)"),    # 0° points right: distance to x=25 is 12.5m
        (90, 12.5, "Up to wall (y=25)"),      # 90° points up: distance to y=25 is 12.5m
        (180, 12.5, "Left to wall (x=0)"),    # 180° points left: distance to x=0 is 12.5m
        (270, 12.5, "Down to wall (y=0)"),    # 270° points down: distance to y=0 is 12.5m
        (45, 17.68, "Diagonal (northeast)"),  # 45° diagonal to corner
    ]
    
    for angle, expected_dist, description in test_angles:
        reading = scan_data[int(angle)]
        # Distance beyond 5m should return 0
        expected_shown = expected_dist if expected_dist <= bot.lidar.max_range else 0.0
        status = "✓" if abs(reading.distance - expected_shown) < 0.1 else "✗"
        
        print(f"{angle:>8}° {expected_dist:>18.2f}m {reading.distance:>16.2f}m {reading.intensity:>10} {status} {description}")
    
    print("-"*70)
    print("\nNote: Distances beyond 5m LIDAR range should return 0 (no detection)")
    
    # Count how many readings are 0 (beyond range)
    zero_readings = sum(1 for r in scan_data if r.distance == 0.0)
    detected_readings = sum(1 for r in scan_data if r.distance > 0.0)
    
    print(f"\nReadings within range (>0): {detected_readings}")
    print(f"Readings beyond range (=0): {zero_readings}")
    print(f"Total readings: {len(scan_data)}")
    
    bot.shutdown()


if __name__ == "__main__":
    main()
