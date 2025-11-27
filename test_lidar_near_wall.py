"""Test LIDAR with bot closer to walls."""

from src.environment import Environment
from src.bot import Bot


def main():
    """Test LIDAR returns correct distances when bot is near walls."""
    
    # Create environment (25m x 25m)
    env = Environment(width=25.0, height=25.0, resolution=0.1)
    
    # Create bot with 5m LIDAR range
    bot = Bot(lidar_frequency=1.0)
    
    # Place bot closer to walls (2m from left and bottom walls)
    env.set_bot_position(x=2.0, y=2.0, orientation=0.0)
    
    # Update bot's environment context
    bot.position = (2.0, 2.0)
    bot.environment_bounds = (25.0, 25.0)
    
    # Initialize and scan
    bot.initialize()
    scan_data = bot.get_lidar_scan()
    
    print("\n" + "="*70)
    print("LIDAR Test Results - Bot Near Walls")
    print("="*70)
    print(f"Bot Position: (2.0, 2.0)")
    print(f"Environment: 25m x 25m")
    print(f"LIDAR Max Range: {bot.lidar.max_range}m")
    print("="*70)
    print(f"{'Angle':>8} {'Expected Distance':>20} {'Actual Distance':>18} {'Intensity':>12} {'Status':>8}")
    print("-"*70)
    
    # Test specific angles
    test_angles = [
        (0, 23.0, "Right to wall (x=25)"),    # 0° points right: distance to x=25 is 23m
        (90, 23.0, "Up to wall (y=25)"),      # 90° points up: distance to y=25 is 23m
        (180, 2.0, "Left to wall (x=0)"),     # 180° points left: distance to x=0 is 2m ✓ WITHIN RANGE
        (270, 2.0, "Down to wall (y=0)"),     # 270° points down: distance to y=0 is 2m ✓ WITHIN RANGE
    ]
    
    for angle, expected_dist, description in test_angles:
        reading = scan_data[int(angle)]
        # Distance beyond 5m should return 0
        expected_shown = expected_dist if expected_dist <= bot.lidar.max_range else 0.0
        
        if expected_shown > 0:
            # Should detect wall
            status = "✓ DETECTED" if reading.distance > 0 else "✗ MISSED"
            error = abs(reading.distance - expected_shown) if reading.distance > 0 else 999
            accuracy = f"(±{error:.2f}m)" if error < 1 else "(BAD)"
        else:
            # Beyond range - should be 0
            status = "✓ OUT OF RANGE" if reading.distance == 0 else "✗ ERROR"
            accuracy = ""
        
        print(f"{angle:>8}° {expected_dist:>18.2f}m {reading.distance:>16.2f}m {reading.intensity:>10} {status:>15} {description} {accuracy}")
    
    print("-"*70)
    
    # Count how many readings are 0 (beyond range)
    zero_readings = sum(1 for r in scan_data if r.distance == 0.0)
    detected_readings = sum(1 for r in scan_data if r.distance > 0.0)
    
    print(f"\nReadings within range (detected, >0): {detected_readings}")
    print(f"Readings beyond range (=0): {zero_readings}")
    print(f"Total readings: {len(scan_data)}")
    
    # Show some detected readings
    print("\nSample of detected readings (within 5m range):")
    print(f"{'Angle':>8} {'Distance':>12} {'Intensity':>12}")
    print("-"*35)
    count = 0
    for i, reading in enumerate(scan_data):
        if reading.distance > 0 and count < 10:
            print(f"{reading.angle:>8.0f}° {reading.distance:>10.2f}m {reading.intensity:>10}")
            count += 1
    
    bot.shutdown()


if __name__ == "__main__":
    main()
