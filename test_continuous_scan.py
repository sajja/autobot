"""Test continuous LIDAR scanning."""

from src.environment import Environment
from src.bot import Bot
import time


def main():
    """Test continuous asynchronous LIDAR scanning."""
    
    # Create environment (25m x 25m)
    env = Environment(width=25.0, height=25.0, resolution=0.1)
    
    # Create bot with 1Hz LIDAR
    bot = Bot(lidar_frequency=1.0)
    
    # Place bot near walls (2m from left and bottom)
    env.set_bot_position(x=2.0, y=2.0, orientation=0.0)
    
    # Update bot's environment context
    bot.position = (2.0, 2.0)
    bot.environment_bounds = (25.0, 25.0)
    
    # Initialize bot
    bot.initialize()
    
    print("\n" + "="*70)
    print("Continuous LIDAR Scanning Test")
    print("="*70)
    print(f"Bot Position: (2.0, 2.0)")
    print(f"Environment: 25m x 25m")
    print(f"LIDAR: {bot.lidar.scan_frequency}Hz continuous scanning")
    print("="*70)
    
    # Define callback to track scans
    scan_count = [0]
    
    def on_scan(scan_data):
        scan_count[0] += 1
        detected = sum(1 for r in scan_data if r.distance > 0)
        print(f"[Scan #{scan_count[0]}] Time: {time.time():.2f} | "
              f"Detected: {detected}/360 points | "
              f"Sample distance: {scan_data[180].distance:.2f}m @ {scan_data[180].angle}°")
    
    # Start continuous scanning
    print("\nStarting continuous LIDAR scanning...")
    bot.start(lidar_callback=on_scan)
    
    # Run for 5 seconds
    print(f"\nScanning for 5 seconds (expecting ~{int(5 * bot.lidar.scan_frequency)} scans)...")
    time.sleep(5)
    
    # Check latest scan
    print("\n" + "-"*70)
    latest = bot.get_latest_lidar_scan()
    if latest:
        detected = sum(1 for r in latest if r.distance > 0)
        print(f"Latest scan: {detected} points detected within 5m range")
        print(f"Sample readings:")
        for angle in [0, 90, 180, 270]:
            reading = latest[angle]
            print(f"  {angle:3d}°: {reading.distance:5.2f}m, intensity {reading.intensity}")
    
    # Stop bot
    print("\n" + "-"*70)
    print("Stopping bot...")
    bot.stop()
    
    print(f"\nTotal scans completed: {scan_count[0]}")
    print(f"Expected scans: ~{int(5 * bot.lidar.scan_frequency)}")
    
    # Shutdown
    bot.shutdown()
    print("\n" + "="*70)
    print("Test completed successfully!")
    print("="*70)


if __name__ == "__main__":
    main()
