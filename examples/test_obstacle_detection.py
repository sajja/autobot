#!/usr/bin/env python3
"""
Test script demonstrating obstacle detection visualization.
Obstacles turn RED when detected by LIDAR, BLACK when not detected.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.bot import Bot
from src.environment import Environment, Position

def main():
    print("="*60)
    print("Obstacle Detection Visualization Test")
    print("="*60)
    print("\nInstructions:")
    print("1. Obstacles start BLACK (not detected)")
    print("2. Click 'Start Bot' to begin LIDAR scanning")
    print("3. Click 'Place Object' then click on the plot to add obstacles")
    print("4. Obstacles turn RED when LIDAR can see them")
    print("5. Obstacles turn BLACK when out of LIDAR range (5m)")
    print("6. Click 'Stop Bot' to stop scanning (all obstacles turn BLACK)")
    print("="*60)
    
    # Create environment
    env = Environment(width=25.0, height=25.0, resolution=0.1)
    print(f"\nEnvironment: Created {env.width}m x {env.height}m environment")
    print(f"Environment: Grid size {env.grid_width} x {env.grid_height} (resolution: {env.resolution}m)")
    
    # Create bot
    bot = Bot(lidar_frequency=1.0)  # 1 Hz LIDAR scanning
    print("Bot: Initialized with 1Hz LIDAR (5m range)")
    
    # Place bot in center
    center_x = env.width / 2
    center_y = env.height / 2
    env.set_bot_position(center_x, center_y, orientation=0.0)
    print(f"Environment: Bot placed at ({center_x:.2f}, {center_y:.2f}) facing 0.0°")
    
    # Add some obstacles at different distances
    # Close obstacle (within 5m range - should be detected)
    env.add_obstacle(center_x + 3.0, center_y, radius=0.15)
    print(f"\nObstacle 1: Added at ({center_x + 3.0:.2f}, {center_y:.2f}) - 3m from bot (SHOULD BE DETECTED)")
    
    # Medium distance obstacle (within 5m range)
    env.add_obstacle(center_x, center_y + 4.0, radius=0.15)
    print(f"Obstacle 2: Added at ({center_x:.2f}, {center_y + 4.0:.2f}) - 4m from bot (SHOULD BE DETECTED)")
    
    # Far obstacle (beyond 5m range - should NOT be detected)
    env.add_obstacle(center_x + 7.0, center_y, radius=0.15)
    print(f"Obstacle 3: Added at ({center_x + 7.0:.2f}, {center_y:.2f}) - 7m from bot (TOO FAR - NOT DETECTED)")
    
    # Diagonal obstacle (just within range)
    env.add_obstacle(center_x + 3.5, center_y + 3.5, radius=0.15)
    print(f"Obstacle 4: Added at ({center_x + 3.5:.2f}, {center_y + 3.5:.2f}) - ~5m from bot (EDGE CASE)")
    
    print("\n" + "="*60)
    print("Opening interactive visualization...")
    print("Watch the obstacle colors change when you start the bot!")
    print("="*60)
    
    # Start visualization
    env.visualize_interactive(bot_instance=bot)

if __name__ == "__main__":
    main()
