"""Interactive demo showing bot control with GUI button."""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.environment import Environment
from src.bot import Bot


def main():
    """Demo interactive environment with bot control."""
    print("=" * 60)
    print("Interactive Bot Control Demo")
    print("=" * 60)
    print()
    
    # Create environment
    print("Creating environment...")
    env = Environment(width=10.0, height=10.0, resolution=0.1)
    
    # Create bot with 1Hz LIDAR frequency
    print("Creating bot with 1Hz LIDAR...")
    bot = Bot(lidar_frequency=1.0)
    
    # Place bot in environment
    print("Placing bot in environment...")
    env.set_bot_position(x=5.0, y=5.0, orientation=0.0)
    
    print()
    print("=" * 60)
    print("INSTRUCTIONS:")
    print("1. A GUI window will open")
    print("2. Click the 'Start Bot' button to begin")
    print("3. The LIDAR scan will run and display results in the console")
    print("4. Close the window when done")
    print("=" * 60)
    print()
    
    input("Press Enter to open interactive GUI...")
    
    # Show interactive visualization
    env.visualize_interactive(bot_instance=bot)
    
    print()
    print("Demo completed!")


if __name__ == "__main__":
    main()
