#!/usr/bin/env python3
"""
Wall Detection Visualization Demo
==================================

This demo shows how LIDAR detects environment boundaries (walls)
and visualizes them as green dots on the plot in real-time.

Features:
- Green dots show where LIDAR rays hit the walls
- Dots update every scan (1Hz)
- Dots disappear when bot stops
- Move bot to different positions to see different wall patterns

Visual Legend:
- 🔵 Blue Bot Circle = Bot running
- 🌀 Cyan Dashed Circle = LIDAR 5m range
- 🟢 Green Dots = Wall detections (LIDAR hits boundaries)
- 🔴 Red Objects = Obstacles detected by LIDAR
- ⚫ Black Objects = Obstacles not detected
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.bot import Bot
from src.environment import Environment

def main():
    print("="*70)
    print("Wall Detection Visualization Demo")
    print("="*70)
    
    print("\n🎯 What This Demonstrates:")
    print("  • LIDAR detects environment boundaries (walls)")
    print("  • Wall detections shown as RED DOTS")
    print("  • Dots appear in real-time as LIDAR scans")
    print("  • Pattern changes based on bot position")
    
    print("\n📍 Recommended Positions to Try:")
    print("  1. Center (12.5, 12.5) - No walls detected (all >5m away)")
    print("  2. Corner (22, 22) - Two walls detected (top + right)")
    print("  3. Edge (22, 12.5) - One wall detected (right)")
    print("  4. Near corner (20, 3) - Two walls (right + bottom)")
    
    print("\n🎨 Visual Legend:")
    print("  � Red Dots      = Wall detections (LIDAR hitting boundaries)")
    print("  🔵 Blue Circle   = Bot (running)")
    print("  🌀 Cyan Circle   = LIDAR range (5m)")
    print("  � Orange Objects = Obstacles detected (if placed)")
    print("  ⚫ Black Objects = Obstacles not detected")
    
    print("\n💡 Instructions:")
    print("  1. Click 'Move Bot' to position the bot near a wall")
    print("  2. Click 'Start Bot' to begin LIDAR scanning")
    print("  3. Watch green dots appear where LIDAR hits walls")
    print("  4. Move bot to different positions to see different patterns")
    print("  5. Add obstacles with 'Place Object' to see difference")
    
    print("\n" + "="*70)
    
    # Create environment
    env = Environment(width=25.0, height=25.0, resolution=0.1)
    
    # Create bot
    bot = Bot(lidar_frequency=1.0)
    
    # Start at center (no walls visible)
    env.set_bot_position(12.5, 12.5, orientation=0.0)
    
    print("\n✅ Bot starts at CENTER (12.5, 12.5)")
    print("   → All walls are >5m away (no wall detections expected)")
    print("\n💡 TIP: Use 'Move Bot' to reposition near a wall!")
    print("   Try (22, 22) for corner detection!")
    
    print("\n" + "="*70)
    print("Opening interactive window...")
    print("="*70 + "\n")
    
    # Start interactive visualization
    env.visualize_interactive(bot_instance=bot)

if __name__ == "__main__":
    main()
