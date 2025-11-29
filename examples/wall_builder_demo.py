#!/usr/bin/env python3
"""
Wall Builder Demo
=================

This demo showcases the new environment controls:
- Reset Environment button (clear all obstacles)
- Horizontal Wall button (place 3m horizontal walls)
- Vertical Wall button (place 3m vertical walls)

Features:
- Build custom environments with walls
- Create mazes and obstacle courses
- Reset and rebuild as needed
- Test bot navigation in custom layouts

Instructions:
1. Click "H-Wall" to place horizontal walls
2. Click "V-Wall" to place vertical walls
3. Click "Place Object" to add circular obstacles
4. Click "Reset Env" to clear everything
5. Click "Start Bot" to test with LIDAR
6. Use arrow keys to navigate your custom environment
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.bot import Bot
from src.environment import Environment

def main():
    print("="*70)
    print("Wall Builder Demo - Create Custom Environments")
    print("="*70)
    
    print("\n🏗️  BUILD YOUR OWN ENVIRONMENT!")
    
    print("\n📐 NEW BUTTONS:")
    print("  ━  H-Wall     = Click to place 3m horizontal wall")
    print("  ┃  V-Wall     = Click to place 3m vertical wall")
    print("  🧹 Reset Env  = Clear all obstacles and walls")
    
    print("\n🎯 EXISTING BUTTONS:")
    print("  🟢 Move Bot      = Reposition the bot")
    print("  🔵 Place Object  = Add circular obstacles")
    print("  🔴 Start Bot     = Begin LIDAR scanning")
    
    print("\n💡 TRY THESE BUILDS:")
    
    print("\n  1. CREATE A MAZE:")
    print("     • Use H-Wall and V-Wall to create corridors")
    print("     • Navigate with arrow keys")
    print("     • Watch LIDAR detect walls")
    
    print("\n  2. BUILD A ROOM:")
    print("     • Place 4 walls to form boundaries")
    print("     • Add obstacles inside")
    print("     • Test navigation inside room")
    
    print("\n  3. OBSTACLE COURSE:")
    print("     • Mix walls and circular obstacles")
    print("     • Create challenging paths")
    print("     • Navigate from start to finish")
    
    print("\n  4. CORNER TRAP:")
    print("     • Build L-shaped walls")
    print("     • Move bot into corner")
    print("     • See RED dots on two walls")
    
    print("\n⚙️  WALL SPECIFICATIONS:")
    print("  • Length: 3 meters")
    print("  • Thickness: 10cm (20cm diameter)")
    print("  • Detection: LIDAR detects as obstacles")
    print("  • Visualization: Black line + obstacle circles")
    
    print("\n🎮 CONTROLS (when bot is running):")
    print("  ⬆️  UP    = Move Forward")
    print("  ⬇️  DOWN  = Move Backward")
    print("  ⬅️  LEFT  = Rotate Left")
    print("  ➡️  RIGHT = Rotate Right")
    
    print("\n" + "="*70)
    
    # Create environment
    env = Environment(width=25.0, height=25.0, resolution=0.1)
    
    # Create bot
    bot = Bot(lidar_frequency=1.0)
    
    # Start at center - empty environment for building
    env.set_bot_position(12.5, 12.5, orientation=0.0)
    
    print("\n✅ Empty environment ready for building")
    print("\n💡 QUICK START:")
    print("  1. Click 'H-Wall' button")
    print("  2. Click on plot to place horizontal wall")
    print("  3. Click 'V-Wall' button")
    print("  4. Click on plot to place vertical wall")
    print("  5. Repeat to build your layout")
    print("  6. Click 'Start Bot' to test")
    print("  7. Click 'Reset Env' to start over")
    
    print("\n" + "="*70)
    print("Opening interactive window...")
    print("="*70)
    print("\n🏗️  BUILD YOUR CUSTOM ENVIRONMENT!\n")
    
    # Start interactive visualization
    env.visualize_interactive(bot_instance=bot)

if __name__ == "__main__":
    main()
