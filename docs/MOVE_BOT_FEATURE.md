# Move Bot Feature - Documentation

## Overview

You can now **change the bot's starting position** before or between scanning sessions using the new "Move Bot" button.

## How to Use

### 1. Move Bot Button
- Click the **green "Move Bot"** button
- Button turns **yellow** and text changes to "Click to Move"
- Click anywhere on the plot to reposition the bot
- Bot moves to the clicked location instantly

### 2. Restrictions
- ⚠️ **Cannot move while running**: Must stop the bot first
- ⚠️ **Minimum distance from obstacles**: 0.5m clearance required
- ⚠️ **Within bounds**: Position must be inside the environment

### 3. Visual Feedback
```
✅ Bot moved from (12.50, 12.50) to (22.28, 3.39)
```

## Button Layout

```
┌─────────────────────────────────────────────────────┐
│                 Environment Plot                    │
│                                                     │
│              [Bot position shown here]              │
│                                                     │
└─────────────────────────────────────────────────────┘
  [Move Bot]    [Start Bot]    [Place Object]
    green          red            blue
```

## Usage Workflow

### Scenario 1: Change Starting Position
```
1. Click "Move Bot" (button turns yellow)
2. Click desired position on plot
3. Bot moves to new location
4. Button automatically returns to green
5. Click "Start Bot" to begin scanning from new position
```

### Scenario 2: Reposition During Operation
```
1. Bot is running (blue with cyan LIDAR circle)
2. Click "Stop Bot" (bot turns red, LIDAR stops)
3. Click "Move Bot" (button turns yellow)
4. Click new position
5. Bot moves to new location
6. Click "Start Bot" to resume from new position
```

### Scenario 3: Strategic Obstacle Testing
```
1. Click "Place Object" to add obstacles at various distances
2. Click "Move Bot" to position bot optimally
3. Click "Start Bot" to see which obstacles are detected (turn red)
4. Click "Stop Bot" and reposition to test different angles
```

## Error Messages

### Too Close to Obstacle
```
❌ Too close to obstacle! Distance: 0.35m (min: 0.5m)
```
Solution: Click further away from obstacles

### Out of Bounds
```
❌ Position (26.50, 13.20) is out of bounds
```
Solution: Click within the environment boundaries (0-25m for default)

### Bot Running
```
⚠️  Cannot move bot while running! Stop the bot first.
```
Solution: Click "Stop Bot" first, then "Move Bot"

## Technical Details

### Implementation
- **Function**: `on_move_bot_clicked()` toggles move mode
- **Handler**: `on_plot_click()` processes mouse clicks
- **Validation**: Checks bounds, obstacle clearance, and bot state
- **Updates**: Redraws bot circle, arrow, text, and LIDAR circle

### Position Updates
When bot moves:
1. Environment bot_position updated
2. Bot instance position updated  
3. LIDAR sensor position updated
4. Visualization elements redrawn
5. Auto-deactivates move mode

### Code Changes

**Modified files**:
- `src/environment.py`:
  - Added `btn_move_bot` button (green)
  - Added `move_bot_mode` state tracking
  - Added `on_move_bot_clicked()` handler
  - Modified `on_plot_click()` to handle bot movement
  - Added bot position validation and obstacle checking

## Interactive Controls Summary

| Button | Color | Function | Restrictions |
|--------|-------|----------|--------------|
| **Move Bot** | 🟢 Green → 🟡 Yellow | Reposition bot | Only when stopped |
| **Start Bot** | 🔴 Red → 🟢 Green | Start LIDAR | Only when stopped |
| **Stop Bot** | 🟢 Green → 🔴 Red | Stop LIDAR | Only when running |
| **Place Object** | 🔵 Blue → 🟡 Yellow | Add obstacle | Anytime |

## Examples

### Run Full Demo
```bash
python3 examples/full_interactive_demo.py
```

### Run Simple Interactive
```bash
python3 examples/simple_interactive.py
```

### Run Obstacle Detection Test
```bash
python3 examples/test_obstacle_detection.py
```

## Tips

💡 **Strategic Positioning**: Move bot close to obstacles (but not too close) to maximize LIDAR detections

💡 **Corner Testing**: Position bot in corners to test wall detection

💡 **Edge Cases**: Move bot to exactly 5m from obstacles to test range limits

💡 **Multi-Obstacle**: Add multiple obstacles, then move bot to different positions to see detection patterns

## Visual States

### Bot Stopped (Ready to Move)
- 🔴 Red circle
- Red arrow showing orientation
- Can be moved with "Move Bot"

### Bot Running (Cannot Move)
- 🔵 Blue circle  
- Blue arrow
- 🌀 Cyan LIDAR circle
- "Move Bot" button disabled

### Moving Mode Active
- 🟡 Yellow "Click to Move" button
- Next click on plot moves bot
- Auto-deactivates after moving

## Future Enhancements

Potential improvements:
- [ ] Rotate bot (change orientation angle)
- [ ] Drag-and-drop bot movement
- [ ] Show movement history trail
- [ ] Snap to grid positioning
- [ ] Keyboard controls (arrow keys)
- [ ] Save/load bot positions
