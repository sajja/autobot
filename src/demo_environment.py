"""Demo script for the environment."""

from environment import Environment, Position


def demo_environment():
    """Demonstrate the Environment class with GUI visualization."""
    print("=" * 60)
    print("Environment Demo - Blank Environment (GUI)")
    print("=" * 60)
    print()
    
    # Create a 10m x 10m environment
    env = Environment(width=10.0, height=10.0, resolution=0.1)
    print()
    
    # Place the bot at the center
    print("--- Placing Bot ---")
    env.set_bot_position(x=5.0, y=5.0, orientation=0.0)
    print()
    
    # Display the environment using GUI
    print("--- Visualizing Environment (GUI) ---")
    print("Close the window to continue...")
    env.visualize(show=True)
    print()
    
    # Get environment info
    print("--- Environment Information ---")
    info = env.get_info()
    for key, value in info.items():
        print(f"{key}: {value}")
    print()
    
    # Test position validation
    print("--- Position Validation ---")
    test_positions = [
        (5.0, 5.0, "Center"),
        #(0.0, 0.0, "Bottom-left corner"),
        #(10.0, 10.0, "Top-right corner"),
        #(15.0, 5.0, "Out of bounds"),
        #(-1.0, 5.0, "Out of bounds"),
    ]
    
    for x, y, description in test_positions:
        valid = env.is_valid_position(x, y)
        status = "✓ Valid" if valid else "✗ Invalid"
        print(f"{description} ({x}, {y}): {status}")
    print()
    
    # Move the bot to different positions and visualize each
    print("--- Moving Bot Around ---")
    new_positions = [
        #(2.0, 2.0, 45.0, "Bottom-left, facing NE"),
        #(8.0, 8.0, 180.0, "Top-right, facing West"),
        #(5.0, 5.0, 270.0, "Center, facing South"),
    ]
    
    for x, y, orientation, description in new_positions:
        env.set_bot_position(x, y, orientation)
        print(f"Visualizing: {description}")
        print("Close the window to continue...")
        env.visualize(show=True)
    
    print()
    
    # Also keep text display for comparison
    print("--- Text Representation (for reference) ---")
    print(env.display())
    print()
    
    print("=" * 60)
    print("Environment demo completed!")
    print("=" * 60)


if __name__ == "__main__":
    demo_environment()
