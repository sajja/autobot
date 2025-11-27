"""Main entry point for the autonomous vehicle bot application."""

from .bot import Bot
import time


def main():
    """Main function demonstrating the Bot class."""
    print("=" * 50)
    print("Autonomous Vehicle Bot - Demo")
    print("=" * 50)
    
    # Create bot instance
    bot = Bot()
    
    try:
        # Initialize all systems
        bot.initialize()
        print()
        
        # Demonstrate sensor readings
        print("--- Sensor Readings ---")
        
        # Get sonar reading
        sonar_reading = bot.get_sonar_distance()
        print(f"Sonar distance: {sonar_reading.distance:.2f} meters")
        
        # Check for obstacles
        obstacle_detected = bot.check_obstacles(threshold=0.5)
        print(f"Obstacle detected (< 0.5m): {obstacle_detected}")
        
        # Get LIDAR scan
        print("\nGetting LIDAR scan (360 degrees)...")
        lidar_scan = bot.get_lidar_scan()
        print(f"LIDAR scan complete: {len(lidar_scan)} data points")
        
        # Perform complete environment scan
        print("\nPerforming complete environment scan...")
        env_scan = bot.scan_environment()
        print(f"Environment scan complete:")
        print(f"  - LIDAR points: {env_scan['lidar']['num_points']}")
        print(f"  - Sonar distance: {env_scan['sonar']['distance']:.2f}m")
        print()
        
        # Demonstrate movement
        print("--- Movement Demonstration ---")
        
        # Move forward safely (checks for obstacles)
        print("\nAttempting to move forward...")
        success = bot.safe_move_forward(steps=100, obstacle_threshold=0.5)
        if success:
            print("Movement completed successfully")
        else:
            print("Movement blocked by obstacle")
        
        # Turn left
        print("\nTurning left...")
        bot.turn_left(steps=50)
        
        # Turn right
        print("\nTurning right...")
        bot.turn_right(steps=50)
        
        # Rotate in place
        print("\nRotating clockwise in place...")
        bot.rotate(steps=100, clockwise=True)
        
        # Move backward
        print("\nMoving backward...")
        bot.move_backward(steps=50)
        
        # Stop all motors
        print("\nStopping all motors...")
        bot.stop()
        
        print()
        print("=" * 50)
        print("Demo completed successfully!")
        print("=" * 50)
        
    except Exception as e:
        print(f"\nError occurred: {e}")
    
    finally:
        # Always shutdown properly
        print("\nShutting down bot...")
        bot.shutdown()


if __name__ == "__main__":
    main()
