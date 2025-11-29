# Wall Builder Features

## Overview

New interactive buttons allow you to build custom environments with walls and obstacles, then reset everything to start fresh.

## New Buttons

### 🧹 Reset Environment
**Color:** Orange  
**Function:** Clears all obstacles and walls from the environment

**Usage:**
1. Click "Reset Env" button
2. All obstacles, walls, and objects are removed
3. Environment returns to empty state
4. Bot position remains unchanged

**Restrictions:**
- Cannot reset while bot is running
- Must stop bot first

**Console Output:**
```
🧹 RESETTING ENVIRONMENT...
Environment: All obstacles removed
✅ Environment reset complete - all obstacles removed
```

---

### ━ Horizontal Wall (H-Wall)
**Color:** Purple  
**Function:** Places a 3-meter horizontal wall at clicked location

**Specifications:**
- **Length:** 3.0 meters
- **Thickness:** 10cm radius (20cm diameter)
- **Segments:** 16 obstacle circles forming wall
- **Visualization:** Black line + obstacle circles

**Usage:**
1. Click "H-Wall" button (turns yellow)
2. Click on plot where you want wall
3. Wall is placed horizontally through click point
4. Button auto-deactivates after placement

**Wall Behavior:**
- Centers on click Y-coordinate
- Extends 1.5m left and right
- Adjusts to fit within boundaries
- Cannot place within 0.5m of bot

**Console Output:**
```
━ HORIZONTAL WALL MODE: Click on plot to place a horizontal wall

━ Placing horizontal wall at y=12.50
Environment: Added obstacle at (11.00, 12.50) with radius 0.10m
Environment: Added obstacle at (11.20, 12.50) with radius 0.10m
...
✅ Horizontal wall placed: 16 segments from (11.00, 12.50) to (14.00, 12.50)
```

---

### ┃ Vertical Wall (V-Wall)
**Color:** Purple  
**Function:** Places a 3-meter vertical wall at clicked location

**Specifications:**
- **Length:** 3.0 meters
- **Thickness:** 10cm radius (20cm diameter)
- **Segments:** 16 obstacle circles forming wall
- **Visualization:** Black line + obstacle circles

**Usage:**
1. Click "V-Wall" button (turns yellow)
2. Click on plot where you want wall
3. Wall is placed vertically through click point
4. Button auto-deactivates after placement

**Wall Behavior:**
- Centers on click X-coordinate
- Extends 1.5m up and down
- Adjusts to fit within boundaries
- Cannot place within 0.5m of bot

**Console Output:**
```
┃ VERTICAL WALL MODE: Click on plot to place a vertical wall

┃ Placing vertical wall at x=12.50
Environment: Added obstacle at (12.50, 11.00) with radius 0.10m
Environment: Added obstacle at (12.50, 11.20) with radius 0.10m
...
✅ Vertical wall placed: 16 segments from (12.50, 11.00) to (12.50, 14.00)
```

---

## Button Layout

```
Second Row:
[H-Wall] [V-Wall]

First Row:
[Move Bot] [Start Bot] [Place Object] [Reset Env]
```

## Use Cases

### 1. Create a Maze
```
Steps:
1. Place multiple H-Walls to create corridors
2. Place V-Walls to create intersections
3. Start bot at one end
4. Navigate to the other end using arrow keys
```

**Example Layout:**
```
━━━━━━━━━━━━━
┃           ┃
┃  ━━━━━    ┃
┃      ┃    ┃
┃  ━━  ┃  ○ ┃  (○ = bot)
┃  ┃       ┃
━━━━━━━━━━━━━
```

### 2. Build a Room
```
Steps:
1. Place H-Wall at top
2. Place H-Wall at bottom
3. Place V-Wall at left
4. Place V-Wall at right
5. Add obstacles inside
6. Test navigation
```

**Example:**
```
━━━━━━━━━━━━━
┃           ┃
┃   ●   ●   ┃  (● = obstacles)
┃     ○     ┃  (○ = bot)
┃   ●   ●   ┃
━━━━━━━━━━━━━
```

### 3. Obstacle Course
```
Steps:
1. Mix H-Walls, V-Walls, and circular obstacles
2. Create challenging navigation path
3. Test bot's ability to detect and avoid
```

**Example:**
```
   ━━━━
   ┃  ●
○  ┃  ━━━
   ●  ┃
━━━━  ┃
      ●
```

### 4. Test Wall Detection
```
Steps:
1. Build L-shaped corner with walls
2. Move bot near corner
3. Start bot
4. See RED dots on both walls
```

**Example:**
```
━━━━━━━━━━━
┃        ○  (○ = bot near corner)
┃        ●● (● = RED dots showing wall detection)
┃        ●●
```

## LIDAR Detection

Walls behave as obstacles:
- Each wall segment is a circular obstacle (10cm radius)
- LIDAR detects walls just like obstacles
- Walls turn RED when detected
- Walls turn BLACK when out of range
- Environment boundaries still show as RED dots

**Detection Pattern:**
```
Bot at center with vertical wall to the right:

        ┃
        ┃ ← Wall detected (RED when in range)
   ○────┃ ← LIDAR scanning
        ┃
        ┃
```

## Technical Details

### Wall Construction

**Horizontal Wall:**
```python
wall_length = 3.0 meters
wall_thickness = 0.1 meter (radius)
num_obstacles = 16
spacing = wall_length / num_obstacles ≈ 0.2m

Obstacles placed at:
(x - 1.5, y), (x - 1.3, y), ..., (x + 1.5, y)
```

**Vertical Wall:**
```python
wall_length = 3.0 meters
wall_thickness = 0.1 meter (radius)
num_obstacles = 16
spacing = wall_length / num_obstacles ≈ 0.2m

Obstacles placed at:
(x, y - 1.5), (x, y - 1.3), ..., (x, y + 1.5)
```

### Collision Safety

Walls cannot be placed:
- Within 0.5m of bot
- Outside environment boundaries
- Overlapping is allowed (for creating corners)

### Reset Behavior

Reset clears:
- All placed obstacles (circular)
- All wall segments
- All wall visualization lines
- All center markers

Reset preserves:
- Bot position
- Bot orientation
- Environment size
- Grid resolution

## Keyboard Controls Integration

Walls work with keyboard controls:
- ✅ Bot can navigate around walls
- ✅ Collision detection prevents hitting walls
- ✅ LIDAR continuously scans walls
- ✅ Arrow keys work normally with walls present

```
Wall present:
━━━━━━
    ┃
○   ┃  ← Press UP (forward)
    ┃
    ┃  ← Collision detected!
    
⚠️  Cannot move forward - obstacle in the way!
```

## Demo Script

Run the wall builder demo:
```bash
python3 examples/wall_builder_demo.py
```

This demo:
- Starts with empty environment
- Shows all button controls
- Provides building suggestions
- Demonstrates wall features

## Examples

### Example 1: Simple Room
```bash
# Steps:
1. Click H-Wall, place at y=15
2. Click H-Wall, place at y=10
3. Click V-Wall, place at x=10
4. Click V-Wall, place at x=15
5. Move bot to center of room
6. Start bot to see all 4 walls detected
```

### Example 2: Corridor
```bash
# Steps:
1. Click H-Wall, place at y=13
2. Click H-Wall, place at y=12
3. Creates 1-meter wide corridor
4. Navigate bot through corridor with arrow keys
```

### Example 3: Complex Maze
```bash
# Steps:
1. Click H-Wall multiple times for horizontal sections
2. Click V-Wall multiple times for vertical sections
3. Build intricate path
4. Start bot at entrance
5. Navigate to exit using keyboard
```

## Tips

💡 **Building Walls:**
- Walls auto-deactivate after placing (one click = one wall)
- Click button again to place another wall
- Use "Reset Env" to clear and start over

💡 **Positioning:**
- Walls center on click point
- Horizontal walls extend left/right from click
- Vertical walls extend up/down from click

💡 **Corners:**
- Place overlapping H-Wall and V-Wall for L-corners
- Create closed rooms by placing 4 walls

💡 **Testing:**
- Build first, then start bot
- Use arrow keys to test navigation
- Watch LIDAR detect walls in real-time

## Summary

✅ **Features Added:**
- Reset Environment button (clear all)
- Horizontal Wall placement (3m walls)
- Vertical Wall placement (3m walls)
- Wall visualization with lines
- Full LIDAR integration
- Keyboard control compatibility

🎯 **Best Demo:**
```bash
python3 examples/wall_builder_demo.py
# Build → Test → Reset → Rebuild!
```
