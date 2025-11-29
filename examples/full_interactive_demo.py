#!/usr/bin/env python3
"""
Full Interactive Demo - All Features
=====================================

Features:
1. Move Bot - Click to change bot starting position
2. Place Objects - Click to add 30cm obstacles
3. Start/Stop Bot - Control LIDAR scanning
4. Visual Feedback - Obstacles turn RED when detected by LIDAR

Controls:
---------
- 'Move Bot' button: Click button, then click plot to move bot
  (Only works when bot is stopped)
  
- 'Start Bot' button: Begin LIDAR scanning
  - Bot turns BLUE (running)
  - LIDAR circle appears (cyan, 5m range)
  - Obstacles within range turn RED
  
- 'Stop Bot' button: Stop LIDAR scanning
  - Bot turns RED (stopped)
  - LIDAR circle disappears
  - All obstacles turn BLACK
  
- 'Place Object' button: Click button, then click plot to add obstacle
  - Obstacle is 30cm diameter
  - Appears BLACK initially
  - Turns RED if bot is running and within 5m range
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.bot import Bot
from src.environment import Environment

def main():
    print("="*70)
    print("Full Interactive Demo - Autonomous Bot Simulator")
    print("="*70)
    
    print("\n📋 Available Controls:")
    print("  🤖 Move Bot     - Reposition the bot (only when stopped)")
    print("  ▶️  Start Bot    - Begin LIDAR scanning (bot turns BLUE)")
    print("  ⏹️  Stop Bot     - Stop LIDAR scanning (bot turns RED)")
    print("  📦 Place Object - Add 30cm obstacles to environment")
    
    print("\n🎨 Visual Indicators:")
    print("  🔴 Red Bot      - Stopped")
    print("  🔵 Blue Bot     - Running with LIDAR")
    print("  ⚫ Black Object - Not detected by LIDAR")
    print("  🔴 Red Object   - Detected by LIDAR (within 5m)")
    print("  🌀 Cyan Circle  - LIDAR range (5m radius)")
    
    print("\n" + "="*70)
    
    # Create environment
    env = Environment(width=25.0, height=25.0, resolution=0.1)
    print(f"\n✅ Environment: {env.width}m × {env.height}m (250 × 250 grid)")
    
    # Create bot
    bot = Bot(lidar_frequency=1.0)  # 1 Hz LIDAR scanning
    print(f"✅ Bot: 1Hz LIDAR, 5m range, 360° coverage")
    
    # Place bot at default position
    center_x = env.width / 2
    center_y = env.height / 2
    env.set_bot_position(center_x, center_y, orientation=0.0)
    print(f"✅ Bot positioned at ({center_x:.2f}, {center_y:.2f})")
    
    print("\n💡 Tip: Use 'Move Bot' to reposition before starting!")
    print("💡 Tip: Add obstacles with 'Place Object' to test detection!")
    
    print("\n" + "="*70)
    print("Opening interactive window...")
    print("="*70 + "\n")
    
    # Start interactive visualization
    env.visualize_interactive(bot_instance=bot)

if __name__ == "__main__":
    main()
