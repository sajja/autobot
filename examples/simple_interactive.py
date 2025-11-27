"""Simple interactive bot demo - just click Start Bot button."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.environment import Environment
from src.bot import Bot


def main():
    """Demo interactive environment with bot control."""
    print("=" * 60)
    print("Interactive Bot Control - LIDAR Demo")
    print("=" * 60)
    
    # Create environment (25m x 25m - larger than LIDAR 10m range)
    env = Environment(width=25.0, height=25.0, resolution=0.1)
    bot = Bot(lidar_frequency=1.0)  # 1Hz LIDAR with 10m range
    
    # Place bot in center
    env.set_bot_position(x=12.5, y=12.5, orientation=0.0)
    
    print("\nEnvironment: 25m x 25m")
    print("LIDAR Range: 10m (cannot scan entire environment)")
    print("\nClick the 'Start Bot' button in the GUI to begin LIDAR scan!")
    print("The scan data will appear in this console.")
    print("Close the window when done.\n")
    
    # Show interactive GUI
    env.visualize_interactive(bot_instance=bot)


if __name__ == "__main__":
    main()
