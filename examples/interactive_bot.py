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
    
    # Create environment (25m x 25m - larger than LIDAR's 10m range)
    print("Creating environment (25m x 25m)...")
    env = Environment(width=25.0, height=25.0, resolution=0.1)
    
    # Create bot with 1Hz LIDAR (10m range)
    print("Creating bot with 1Hz LIDAR (10m max range)...")
    bot = Bot(lidar_frequency=1.0)
    
    # Place bot in environment
    print("Placing bot in environment center...")
    env.set_bot_position(x=12.5, y=12.5, orientation=0.0)
    
    print()
    print("=" * 60)
    print("INSTRUCTIONS:")
    print("1. A GUI window will open showing a 25m x 25m environment")
    print("2. The bot is in the center with 10m LIDAR range")
    print("3. LIDAR cannot scan the entire environment from this position")
    print("4. Click the 'Start Bot' button to begin")
    print("5. The LIDAR scan will run and display results in the console")
    print("6. Close the window when done")
    print("=" * 60)
    print()
    
    input("Press Enter to open interactive GUI...")
    
    # Show interactive visualization
    env.visualize_interactive(bot_instance=bot)
    
    print()
    print("Demo completed!")


if __name__ == "__main__":
    main()
