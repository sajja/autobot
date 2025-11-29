#!/usr/bin/env python3
"""
LIDAR Output Demo - Bot at Corner Position (22, 22)
Shows what LIDAR sees when bot is near top-right corner
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.bot import Bot
from src.environment import Environment

def main():
    print("="*70)
    print("LIDAR Reading Sample - Bot at Corner Position (22, 22)")
    print("="*70)
    
    # Create environment
    env = Environment(width=25.0, height=25.0, resolution=0.1)
    
    # Create bot
    bot = Bot(lidar_frequency=1.0)
    
    # Place bot near top-right corner
    bot_x, bot_y = 22.0, 22.0
    env.set_bot_position(bot_x, bot_y, orientation=0.0)
    
    print(f"\n📍 Bot Position: ({bot_x}, {bot_y})")
    print(f"📏 Environment: {env.width}m × {env.height}m")
    print(f"📡 LIDAR: 5m max range, 360° coverage\n")
    
    print("Distance to walls:")
    print(f"  • Right wall (x=25):  {25 - bot_x}m")
    print(f"  • Top wall (y=25):    {25 - bot_y}m")
    print(f"  • Left wall (x=0):    {bot_x}m")
    print(f"  • Bottom wall (y=0):  {bot_y}m")
    
    # Initialize bot
    bot.initialize()
    
    # Set environment context for LIDAR
    bot.position = (bot_x, bot_y)
    bot.environment_bounds = (env.width, env.height)
    bot.lidar.position = (bot_x, bot_y)
    bot.lidar.environment_bounds = (env.width, env.height)
    bot.lidar.obstacles = env.obstacles
    
    # Get a LIDAR scan
    scan_data = bot.lidar.get_scan()
    
    print("\n" + "="*70)
    print("360° LIDAR SCAN RESULTS")
    print("="*70)
    print(f"{'Angle':<10} {'Direction':<15} {'Distance':<12} {'Intensity':<10} {'Detection'}")
    print("-"*70)
    
    # Show key angles
    key_angles = [0, 45, 90, 135, 180, 225, 270, 315]
    directions = ['East →', 'NE ↗', 'North ↑', 'NW ↖', 'West ←', 'SW ↙', 'South ↓', 'SE ↘']
    
    for i, angle in enumerate(key_angles):
        reading = scan_data[angle]
        detected = "✅ WALL" if reading.distance > 0 else "❌ No detection"
        print(f"{angle:<10}° {directions[i]:<15} {reading.distance:<12.2f}m {reading.intensity:<10} {detected}")
    
    print("\n" + "="*70)
    print("FULL 360° SCAN DATA (showing all non-zero readings)")
    print("="*70)
    print(f"{'Angle (°)':<12} {'Distance (m)':<15} {'Intensity':<15}")
    print("-"*70)
    
    detected_count = 0
    for reading in scan_data:
        if reading.distance > 0:
            print(f"{reading.angle:<12.0f} {reading.distance:<15.2f} {reading.intensity:<15}")
            detected_count += 1
    
    print("-"*70)
    print(f"\nTotal angles with detection: {detected_count}/360")
    print(f"Detection rate: {detected_count/360*100:.1f}%")
    
    print("\n" + "="*70)
    print("ANALYSIS")
    print("="*70)
    print(f"✅ DETECTED: Angles where wall is within 5m LIDAR range")
    print(f"❌ NOT DETECTED: Angles where wall is beyond 5m range")
    
    # Calculate which angles should detect walls
    print("\nExpected detections:")
    print(f"  • 0° (East):   {25-bot_x}m → {'DETECTED' if 25-bot_x <= 5 else 'OUT OF RANGE'}")
    print(f"  • 90° (North): {25-bot_y}m → {'DETECTED' if 25-bot_y <= 5 else 'OUT OF RANGE'}")
    print(f"  • 180° (West): {bot_x}m → {'DETECTED' if bot_x <= 5 else 'OUT OF RANGE'}")
    print(f"  • 270° (South): {bot_y}m → {'DETECTED' if bot_y <= 5 else 'OUT OF RANGE'}")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    main()
