#!/usr/bin/env python3
"""
Simple Wall Detection Test - Shows green dots for wall detections
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.bot import Bot
from src.environment import Environment
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np

def main():
    print("="*70)
    print("Simple Wall Detection Test")
    print("="*70)
    
    # Create environment and bot
    env = Environment(width=25.0, height=25.0, resolution=0.1)
    bot = Bot(lidar_frequency=1.0)
    
    # Place bot near corner (22, 22)
    env.set_bot_position(22.0, 22.0, orientation=0.0)
    print("\n📍 Bot Position: (22.0, 22.0) - near top-right corner")
    print("   Expected: Green dots on RIGHT wall (x=25) and TOP wall (y=25)\n")
    
    # Initialize bot
    bot.initialize()
    bot.position = (22.0, 22.0)
    bot.environment_bounds = (25.0, 25.0)
    bot.lidar.position = (22.0, 22.0)
    bot.lidar.environment_bounds = (25.0, 25.0)
    bot.lidar.obstacles = env.obstacles
    
    # Get LIDAR scan
    print("🔄 Performing LIDAR scan...")
    scan_data = bot.lidar.get_scan()
    
    # Analyze wall detections
    wall_detections = []
    bot_x, bot_y = 22.0, 22.0
    
    for reading in scan_data:
        if reading.distance > 0:
            angle_rad = np.radians(reading.angle)
            detected_x = bot_x + reading.distance * np.cos(angle_rad)
            detected_y = bot_y + reading.distance * np.sin(angle_rad)
            
            # Check if wall
            tolerance = 0.2
            is_wall = False
            wall_name = ""
            
            if abs(detected_x - 0) < tolerance:
                is_wall = True
                wall_name = "Left"
            elif abs(detected_x - 25.0) < tolerance:
                is_wall = True
                wall_name = "Right"
            elif abs(detected_y - 0) < tolerance:
                is_wall = True
                wall_name = "Bottom"
            elif abs(detected_y - 25.0) < tolerance:
                is_wall = True
                wall_name = "Top"
            
            if is_wall:
                wall_detections.append((detected_x, detected_y, wall_name, reading.angle))
    
    print(f"✅ Found {len(wall_detections)} wall detection points\n")
    
    # Show sample detections
    print("Sample wall detections (first 10):")
    print(f"{'Angle':<8} {'Wall':<10} {'X':<8} {'Y':<8}")
    print("-"*40)
    for i, (x, y, wall, angle) in enumerate(wall_detections[:10]):
        print(f"{angle:<8.0f}° {wall:<10} {x:<8.2f} {y:<8.2f}")
    print("...")
    
    # Create visualization
    print("\n📊 Creating visualization...")
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Plot environment boundary
    ax.plot([0, 25, 25, 0, 0], [0, 0, 25, 25, 0], 'k-', linewidth=2, label='Environment Boundary')
    
    # Plot bot
    bot_circle = Circle((bot_x, bot_y), 0.3, color='blue', alpha=0.7, label='Bot')
    ax.add_patch(bot_circle)
    ax.arrow(bot_x, bot_y, 0.5, 0, head_width=0.15, head_length=0.1, 
             fc='darkblue', ec='darkblue', linewidth=2)
    
    # Plot LIDAR range
    lidar_circle = Circle((bot_x, bot_y), 5.0, fill=False, edgecolor='cyan', 
                          linewidth=2, linestyle='--', alpha=0.6, label='LIDAR Range (5m)')
    ax.add_patch(lidar_circle)
    
    # Plot wall detections as GREEN DOTS
    if wall_detections:
        wall_x = [pos[0] for pos in wall_detections]
        wall_y = [pos[1] for pos in wall_detections]
        ax.plot(wall_x, wall_y, 'go', markersize=5, alpha=0.7, label=f'Wall Detections ({len(wall_detections)})')
        print(f"🟢 Plotted {len(wall_detections)} GREEN dots for wall detections")
    
    # Configure plot
    ax.set_xlim(0, 25)
    ax.set_ylim(0, 25)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('X (meters)', fontsize=12)
    ax.set_ylabel('Y (meters)', fontsize=12)
    ax.set_title('Wall Detection Visualization - Green Dots Show LIDAR Hits on Walls', 
                 fontsize=14, fontweight='bold')
    ax.legend(loc='upper left')
    
    # Add text annotation
    ax.text(12.5, 23, 'TOP WALL\n(Green dots)', ha='center', fontsize=10, 
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))
    ax.text(23.5, 12.5, 'RIGHT\nWALL\n(Green\ndots)', ha='center', fontsize=10,
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))
    
    print("\n✅ Visualization created!")
    print("🟢 Look for GREEN DOTS on the top and right walls")
    print("   The dots show where LIDAR rays hit the environment boundaries")
    
    plt.tight_layout()
    plt.show()
    
    print("\n" + "="*70)

if __name__ == "__main__":
    main()
