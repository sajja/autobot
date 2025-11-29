# Keyboard Controls - Quick Reference

## Controls (Bot Must Be Running)

| Key | Action | Movement |
|-----|--------|----------|
| ⬆️ **UP** | Forward | 0.5m in facing direction |
| ⬇️ **DOWN** | Backward | 0.5m opposite direction |
| ⬅️ **LEFT** | Rotate Left | 15° counter-clockwise |
| ➡️ **RIGHT** | Rotate Right | 15° clockwise |

## Quick Start

```bash
# Run the demo
python3 examples/keyboard_control_demo.py

# Steps:
1. Window opens with bot at center
2. Click "Start Bot" button (turns GREEN)
3. Bot turns BLUE (running state)
4. Use arrow keys to control!
```

## Movement Logic

### Forward/Backward
- Movement direction based on bot's current orientation
- Example: If facing East (0°), UP moves right (+X)
- Example: If facing North (90°), UP moves up (+Y)

### Rotation
- Rotates on center axis
- Position (x, y) stays the same
- Only orientation angle changes

## Safety Features

✅ **Collision Detection:**
- Cannot move outside boundaries
- Cannot move through obstacles
- Console warning if blocked

✅ **State Protection:**
- Controls only work when bot is RUNNING
- Cannot move while bot is STOPPED (RED)

## Console Feedback

```bash
# Movement
🔼 Forward: (12.50, 12.50) → (13.00, 12.50)
🔽 Backward: (13.00, 12.50) → (12.50, 12.50)

# Rotation
↺ Rotate Left: 0° → 15°
↻ Rotate Right: 15° → 0°

# Blocked
⚠️  Cannot move forward - would hit boundary!
⚠️  Cannot move backward - obstacle in the way!
```

## Integration with LIDAR

- LIDAR automatically updates from new position
- Wall detection (RED dots) updates as you move
- Obstacle colors update based on distance
- Continuous 1Hz scanning while moving

## Tips

💡 **Navigate to corner for wall detection:**
```
1. Start bot
2. Press UP many times to reach edge
3. Press LEFT to turn 90°
4. Press UP to reach corner
5. See RED L-shape (two walls detected!)
```

💡 **Precise positioning:**
- Current step: 0.5m per key press
- Small increments for accurate navigation
- Check position in bot text label

💡 **Avoid obstacles:**
- Rotate first to face open direction
- Then move forward
- Watch console for collision warnings

## Documentation

- Full guide: `docs/KEYBOARD_CONTROLS.md`
- Demo script: `examples/keyboard_control_demo.py`
- Tests: `tests/test_keyboard_controls.py`
