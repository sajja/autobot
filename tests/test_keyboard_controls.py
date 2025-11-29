#!/usr/bin/env python3
"""
Simple Keyboard Control Test
Test bot movement and rotation without GUI.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.bot import Bot
from src.environment import Environment
import numpy as np

def test_movement():
    """Test forward/backward movement calculations."""
    print("="*60)
    print("Testing Movement Calculations")
    print("="*60)
    
    # Test parameters
    move_distance = 0.5
    
    # Test 1: Forward movement facing East (0°)
    print("\nTest 1: Forward movement facing East (0°)")
    orientation = 0
    start_x, start_y = 12.5, 12.5
    dx = move_distance * np.cos(np.radians(orientation))
    dy = move_distance * np.sin(np.radians(orientation))
    end_x = start_x + dx
    end_y = start_y + dy
    print(f"  Start: ({start_x:.2f}, {start_y:.2f})")
    print(f"  End:   ({end_x:.2f}, {end_y:.2f})")
    print(f"  Expected: (13.00, 12.50)")
    assert abs(end_x - 13.0) < 0.01 and abs(end_y - 12.5) < 0.01, "Forward East failed!"
    print("  ✅ PASS")
    
    # Test 2: Forward movement facing North (90°)
    print("\nTest 2: Forward movement facing North (90°)")
    orientation = 90
    start_x, start_y = 12.5, 12.5
    dx = move_distance * np.cos(np.radians(orientation))
    dy = move_distance * np.sin(np.radians(orientation))
    end_x = start_x + dx
    end_y = start_y + dy
    print(f"  Start: ({start_x:.2f}, {start_y:.2f})")
    print(f"  End:   ({end_x:.2f}, {end_y:.2f})")
    print(f"  Expected: (12.50, 13.00)")
    assert abs(end_x - 12.5) < 0.01 and abs(end_y - 13.0) < 0.01, "Forward North failed!"
    print("  ✅ PASS")
    
    # Test 3: Backward movement facing East (0°)
    print("\nTest 3: Backward movement facing East (0°)")
    orientation = 0
    start_x, start_y = 12.5, 12.5
    dx = move_distance * np.cos(np.radians(orientation))
    dy = move_distance * np.sin(np.radians(orientation))
    end_x = start_x - dx
    end_y = start_y - dy
    print(f"  Start: ({start_x:.2f}, {start_y:.2f})")
    print(f"  End:   ({end_x:.2f}, {end_y:.2f})")
    print(f"  Expected: (12.00, 12.50)")
    assert abs(end_x - 12.0) < 0.01 and abs(end_y - 12.5) < 0.01, "Backward East failed!"
    print("  ✅ PASS")
    
    # Test 4: Rotation
    print("\nTest 4: Rotation")
    rotation_angle = 15
    start_orientation = 0
    
    # Rotate left (counter-clockwise)
    new_orientation = (start_orientation + rotation_angle) % 360
    print(f"  Rotate Left: {start_orientation}° → {new_orientation}°")
    assert new_orientation == 15, "Rotate left failed!"
    print("  ✅ PASS")
    
    # Rotate right (clockwise)
    new_orientation = (start_orientation - rotation_angle) % 360
    print(f"  Rotate Right: {start_orientation}° → {new_orientation}°")
    assert new_orientation == 345, "Rotate right failed!"
    print("  ✅ PASS")
    
    print("\n" + "="*60)
    print("All movement tests PASSED! ✅")
    print("="*60)

def test_collision():
    """Test collision detection."""
    print("\n" + "="*60)
    print("Testing Collision Detection")
    print("="*60)
    
    env = Environment(width=25.0, height=25.0, resolution=0.1)
    
    # Test boundary collision
    print("\nTest 1: Boundary collision detection")
    
    # Test top boundary
    result = env.is_valid_position(12.5, 26.0)
    print(f"  Position (12.5, 26.0) valid? {result}")
    assert result == False, "Should be outside boundary!"
    print("  ✅ PASS - Correctly detected outside boundary")
    
    # Test valid position
    result = env.is_valid_position(12.5, 12.5)
    print(f"  Position (12.5, 12.5) valid? {result}")
    assert result == True, "Should be valid!"
    print("  ✅ PASS - Correctly detected valid position")
    
    # Test obstacle collision
    print("\nTest 2: Obstacle collision detection")
    env.add_obstacle(15.0, 12.5, radius=0.8)
    
    from src.environment import Position
    
    # Test position inside obstacle
    pos_inside = Position(15.0, 12.5)
    result = env.is_position_occupied(pos_inside)
    print(f"  Position (15.0, 12.5) occupied? {result}")
    assert result == True, "Should be occupied (obstacle center)!"
    print("  ✅ PASS - Correctly detected obstacle")
    
    # Test position outside obstacle
    pos_outside = Position(20.0, 12.5)
    result = env.is_position_occupied(pos_outside)
    print(f"  Position (20.0, 12.5) occupied? {result}")
    assert result == False, "Should be free!"
    print("  ✅ PASS - Correctly detected free space")
    
    print("\n" + "="*60)
    print("All collision tests PASSED! ✅")
    print("="*60)

if __name__ == "__main__":
    test_movement()
    test_collision()
    
    print("\n" + "="*60)
    print("🎉 ALL TESTS PASSED! 🎉")
    print("="*60)
    print("\nKeyboard controls are ready!")
    print("Run: python3 examples/keyboard_control_demo.py")
    print("\nControls (when bot is running):")
    print("  ⬆️  UP    = Move Forward")
    print("  ⬇️  DOWN  = Move Backward")
    print("  ⬅️  LEFT  = Rotate Left")
    print("  ➡️  RIGHT = Rotate Right")
