#!/usr/bin/env python3
"""
Keyboard Control Demo
=====================

This demo shows how to control the bot using keyboard arrow keys.

Controls (Bot must be RUNNING/Started):
- UP Arrow:    Move forward (0.5m per press)
- DOWN Arrow:  Move backward (0.5m per press)
- LEFT Arrow:  Rotate counter-clockwise (15° per press)
- RIGHT Arrow: Rotate clockwise (15° per press)

Features:
- Bot only moves when running (started)
- Collision detection with boundaries
- Collision detection with obstacles
- LIDAR updates in real-time as bot moves
- Wall detection shows RED dots as bot moves near walls

Instructions:
1. Click "Start Bot" button to enable movement
2. Use arrow keys to control the bot
3. Watch LIDAR detect obstacles and walls in real-time
4. Try moving near walls to see RED dot patterns
5. Add obstacles with "Place Object" button
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.bot import Bot
from src.environment import Environment

def main():
    print("="*70)
    print("Keyboard Control Demo")
    print("="*70)
    
    print("\n🎮 KEYBOARD CONTROLS (when bot is running):")
    print("  ⬆️  UP Arrow    = Move Forward (0.5m)")
    print("  ⬇️  DOWN Arrow  = Move Backward (0.5m)")
    print("  ⬅️  LEFT Arrow  = Rotate Left (15°)")
    print("  ➡️  RIGHT Arrow = Rotate Right (15°)")
    
    print("\n⚠️  IMPORTANT:")
    print("  • Bot MUST be started (click 'Start Bot' button)")
    print("  • Movement only works when bot is RUNNING (blue)")
    print("  • Collision detection prevents hitting obstacles/walls")
    
    print("\n💡 TRY THIS:")
    print("  1. Click 'Start Bot' to begin")
    print("  2. Press UP arrow several times to move forward")
    print("  3. Press LEFT/RIGHT arrows to rotate")
    print("  4. Move near corner to see wall detection (RED dots)")
    print("  5. Add obstacles with 'Place Object' button")
    print("  6. Try navigating around obstacles")
    
    print("\n🎯 DEMONSTRATION SCENARIO:")
    print("  • Bot starts at (12.5, 12.5) facing East (0°)")
    print("  • Pre-placed obstacles for navigation challenge")
    print("  • Move to corner (22, 22) to see wall detection")
    
    print("\n" + "="*70)
    
    # Create environment
    env = Environment(width=25.0, height=25.0, resolution=0.1)
    
    # Add some obstacles for navigation challenge
    print("\n📦 Adding obstacles...")
    env.add_obstacle(15.0, 12.5, radius=0.8)  # Center-right
    env.add_obstacle(10.0, 10.0, radius=0.6)  # Bottom-left area
    env.add_obstacle(18.0, 18.0, radius=0.7)  # Top-right area
    env.add_obstacle(8.0, 15.0, radius=0.5)   # Left-center
    
    print(f"✅ {len(env.obstacles)} obstacles placed")
    
    # Create bot
    bot = Bot(lidar_frequency=1.0)
    
    # Start at center facing east
    env.set_bot_position(12.5, 12.5, orientation=0.0)
    
    print("\n✅ Bot positioned at CENTER (12.5, 12.5) facing EAST (0°)")
    print("\n💡 NEXT STEPS:")
    print("  1. Window will open with bot at center")
    print("  2. Click 'Start Bot' button (turns GREEN)")
    print("  3. Use arrow keys to navigate:")
    print("     • UP to move forward")
    print("     • DOWN to move backward")
    print("     • LEFT/RIGHT to rotate")
    print("  4. Navigate to top-right corner (22, 22) to see walls!")
    
    print("\n" + "="*70)
    print("Opening interactive window...")
    print("="*70)
    print("\n🎮 Use ARROW KEYS to control (after starting bot)!\n")
    
    # Start interactive visualization with keyboard controls
    env.visualize_interactive(bot_instance=bot)

if __name__ == "__main__":
    main()
