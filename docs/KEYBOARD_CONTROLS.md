# Keyboard Controls Documentation

## Overview

The bot can be controlled using keyboard arrow keys for movement and rotation. **The bot must be in RUNNING state** (started via the "Start Bot" button) to respond to keyboard commands.

## Control Scheme

### Arrow Keys

| Key | Action | Movement | Details |
|-----|--------|----------|---------|
| ⬆️ **UP** | Move Forward | 0.5m per press | Moves in the direction bot is facing |
| ⬇️ **DOWN** | Move Backward | 0.5m per press | Moves opposite to facing direction |
| ⬅️ **LEFT** | Rotate Left | 15° per press | Counter-clockwise rotation on center axis |
| ➡️ **RIGHT** | Rotate Right | 15° per press | Clockwise rotation on center axis |

## Movement Mechanics

### Forward/Backward Movement

```
Bot facing East (0°):
    UP   → Move right (+X direction)
    DOWN → Move left (-X direction)

Bot facing North (90°):
    UP   → Move up (+Y direction)
    DOWN → Move down (-Y direction)

Bot facing West (180°):
    UP   → Move left (-X direction)
    DOWN → Move right (+X direction)

Bot facing South (270°):
    UP   → Move down (-Y direction)
    DOWN → Move up (+Y direction)
```

### Rotation (on Center Axis)

- Bot rotates around its center point
- Position (x, y) remains unchanged during rotation
- Only orientation angle changes

```
Initial: Bot at (12.5, 12.5) facing 0°

LEFT key:  (12.5, 12.5) @ 0°   →  (12.5, 12.5) @ 15°
LEFT key:  (12.5, 12.5) @ 15°  →  (12.5, 12.5) @ 30°
RIGHT key: (12.5, 12.5) @ 30°  →  (12.5, 12.5) @ 15°
```

## Requirements

### Bot Must Be Running

✅ **Allowed:**
```
1. Click "Start Bot" button (turns GREEN, bot turns BLUE)
2. Press arrow keys → Bot moves/rotates
```

❌ **Not Allowed:**
```
1. Bot is stopped (RED)
2. Press arrow keys → Warning message, no movement
```

Console output when trying to move while stopped:
```
⚠️  Bot must be started to move! (Key pressed: up)
```

## Collision Detection

### Boundary Collision

Bot cannot move outside environment boundaries:

```
Bot at (24.5, 12.5) facing East (0°)
Press UP (forward) → Would go to (25.0, 12.5)
Result: ⚠️  Cannot move forward - would hit boundary!
```

### Obstacle Collision

Bot cannot move through obstacles:

```
Bot at (10.0, 12.5), Obstacle at (11.0, 12.5)
Press UP (forward toward obstacle)
Result: ⚠️  Cannot move forward - obstacle in the way!
```

### Rotation Never Collides

Rotation is always allowed (even near obstacles):
- Bot rotates on center axis
- Position doesn't change
- No collision possible

## Visual Feedback

### Console Output

Every movement prints feedback:

```bash
# Forward movement
🔼 Forward: (12.50, 12.50) → (13.00, 12.50)

# Backward movement
🔽 Backward: (13.00, 12.50) → (12.50, 12.50)

# Rotation left
↺ Rotate Left: 0° → 15°

# Rotation right
↻ Rotate Right: 15° → 0°

# Collision with boundary
⚠️  Cannot move forward - would hit boundary!

# Collision with obstacle
⚠️  Cannot move backward - obstacle in the way!
```

### Visual Updates

When bot moves/rotates:
1. Bot circle position updates (if moved)
2. Direction arrow updates (rotation or movement)
3. Bot text updates with new position and orientation
4. LIDAR circle moves with bot
5. LIDAR re-scans automatically (1Hz continuous)
6. Wall detections update (RED dots)
7. Obstacle colors update (RED=detected, BLACK=not detected)

## Real-Time LIDAR Integration

### Automatic Scanning

When bot is running:
- LIDAR scans continuously at 1Hz
- Each movement triggers automatic position update
- Next LIDAR scan uses new position
- Detections update in real-time

### Detection Updates

```
Bot at (12.5, 12.5) - No walls in range
→ No RED dots

Press UP several times to reach (22, 12.5)
→ Right wall detected
→ RED dots appear on right boundary

Press LEFT to rotate toward corner
Press UP to move forward
→ Reach (22, 22)
→ Two walls detected (right + top)
→ RED dots form L-shape
```

## Usage Examples

### Example 1: Navigate to Corner

```python
# Demo: Navigate from center to top-right corner
# Goal: See wall detection (RED L-shape)

1. Start: Bot at (12.5, 12.5) @ 0° (facing East)
2. Click "Start Bot"
3. Press UP × 19 times → Reach (~22, 12.5)
   - Watch for right wall RED dots
4. Press LEFT × 6 times → Rotate to 90° (facing North)
5. Press UP × 19 times → Reach (~22, 22)
   - Watch RED dots form L-shape (2 walls)
```

### Example 2: Navigate Around Obstacle

```python
# Demo: Avoid obstacle at (15, 12.5)

1. Start: Bot at (12.5, 12.5) @ 0°
2. Click "Start Bot"
3. Press UP × 4 times → Reach (14.5, 12.5)
4. Press LEFT × 6 times → Rotate to 90° (North)
5. Press UP × 4 times → Move up (14.5, 14.5)
6. Press RIGHT × 6 times → Rotate to 0° (East)
7. Press UP × 4 times → Move right (16.5, 14.5)
8. Press RIGHT × 6 times → Rotate to 270° (South)
9. Press UP × 4 times → Move down (16.5, 12.5)
   - Successfully navigated around obstacle!
```

### Example 3: 360° Tour

```python
# Demo: Rotate in place and observe LIDAR

1. Start: Bot at (12.5, 12.5) @ 0°
2. Click "Start Bot"
3. Press LEFT × 24 times → Full 360° rotation
   - Watch LIDAR circle rotate
   - All obstacle colors may change
   - Console shows rotation: 0° → 15° → 30° → ... → 360° (0°)
```

## Demo Script

Run the keyboard control demo:

```bash
python3 examples/keyboard_control_demo.py
```

This demo includes:
- Pre-placed obstacles for navigation challenge
- Instructions for reaching corner (wall detection)
- Real-time LIDAR visualization
- Console feedback for every movement

## Parameters (Customizable)

Current settings in `src/environment.py`:

```python
# Movement distance per key press
move_distance = 0.5  # meters (0.5m = 50cm)

# Rotation angle per key press
rotation_angle = 15  # degrees
```

### To Customize:

Edit these values for different control sensitivity:

```python
# Faster movement
move_distance = 1.0  # 1 meter per press

# Finer rotation control
rotation_angle = 5  # 5 degrees per press

# Slower, more precise
move_distance = 0.1  # 10cm per press
rotation_angle = 1   # 1 degree per press
```

## Troubleshooting

### Issue: Keyboard doesn't work

**Cause:** Bot is not running

**Solution:**
1. Click "Start Bot" button
2. Button should turn GREEN
3. Bot should turn BLUE
4. Try arrow keys again

---

### Issue: Bot moves erratically

**Cause:** Holding down key triggers multiple movements

**Solution:**
- Press and release keys individually
- Wait for visual update between presses
- Don't hold down arrow keys

---

### Issue: Can't move in desired direction

**Cause:** Bot orientation doesn't match intended direction

**Solution:**
1. Check bot's current orientation (arrow shows direction)
2. Use LEFT/RIGHT to rotate bot to face desired direction
3. Then use UP to move forward in that direction

Example:
```
Want to move North (up on screen)?
1. Check orientation angle in bot text
2. Rotate until angle = 90° (facing North)
3. Press UP to move North
```

---

### Issue: Movement seems blocked

**Cause:** Obstacle or boundary in the way

**Solution:**
- Check console for collision warnings
- Rotate to different direction with LEFT/RIGHT
- Move around obstacle

## Advanced Tips

### Precise Positioning

For accurate positioning:
1. Use rotation to face exact direction
2. Use small movements (current: 0.5m)
3. Check position in bot text label
4. Use "Move Bot" button for instant repositioning

### Wall Detection Navigation

To maximize wall detection (RED dots):
1. Navigate to corners (e.g., 22, 22)
2. Stay within 5m of walls (LIDAR range)
3. Rotate to face different walls
4. Watch RED dot patterns change

### Obstacle Detection

To see obstacle color changes:
1. Start far from obstacles (all BLACK)
2. Move toward obstacle using arrow keys
3. When within 5m LIDAR range → Turns RED
4. Move away → Returns to BLACK

## Summary

✅ **Working Features:**
- ⬆️⬇️⬅️➡️ Arrow key controls (when running)
- Forward/backward movement (0.5m per press)
- Rotation on center axis (15° per press)
- Collision detection (boundaries + obstacles)
- Real-time LIDAR updates
- Visual and console feedback
- Automatic bot state synchronization

🎮 **Best Demo:**
```bash
python3 examples/keyboard_control_demo.py
# Start bot → Navigate to corner with arrow keys → See walls!
```
