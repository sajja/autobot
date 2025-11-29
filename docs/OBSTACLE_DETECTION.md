# Obstacle Detection Visualization

## Overview

Obstacles now change color based on whether the bot's LIDAR can detect them:
- **BLACK**: Obstacle is NOT detected (out of LIDAR range or stopped)
- **RED**: Obstacle IS detected by LIDAR (within 5m range and visible)

## How It Works

### 1. LIDAR Ray-Circle Intersection

The LIDAR sensor now performs ray-circle intersection calculations to detect obstacles:

```python
# For each obstacle:
#   Ray: P = (x, y) + t * (dx, dy)
#   Circle: (P_x - obs_x)^2 + (P_y - obs_y)^2 = obs_radius^2
#   Solve quadratic equation to find intersection
```

### 2. Real-time Color Updates

On each LIDAR scan (1Hz frequency), the system:
1. Gets all 360 LIDAR readings with distances
2. Calculates detected positions from bot position and angles
3. Checks which obstacles are within detection range
4. Updates obstacle colors: RED (detected) or BLACK (not detected)

### 3. Visual Feedback

- **Bot Stopped**: All obstacles are BLACK
- **Bot Running**: 
  - Obstacles within 5m LIDAR range → RED
  - Obstacles beyond 5m range → BLACK
  - Colors update every scan (1Hz)

## Code Changes

### Modified Files

1. **src/sensors.py**:
   - Added `obstacles` list to LIDAR sensor
   - Modified `_simulate_reading()` to check obstacles using ray-circle intersection
   - Returns actual distance to nearest obstacle or wall

2. **src/environment.py**:
   - Obstacles drawn as BLACK circles initially
   - Added `update_obstacle_visibility()` function
   - Called on each LIDAR scan to update colors
   - Resets all obstacles to BLACK when bot stops

## Testing

### Run the demo:
```bash
python3 examples/test_obstacle_detection.py
```

### What you'll see:
1. Window opens with 4 obstacles (all BLACK)
2. Click "Start Bot"
3. Obstacles within 5m turn RED immediately
4. Obstacle at 7m stays BLACK (out of range)
5. Click "Stop Bot" - all obstacles turn BLACK again
6. Click "Place Object" to add more obstacles interactively

### Expected Results:
- **Obstacle 1** (3m away): RED when running ✅
- **Obstacle 2** (4m away): RED when running ✅
- **Obstacle 3** (7m away): BLACK (out of range) ✅
- **Obstacle 4** (~5m away): May flicker (edge case) ⚠️

## Interactive Placement

1. Click "Place Object" button (turns yellow)
2. Click anywhere on the plot to place a 30cm obstacle
3. Obstacle appears BLACK initially
4. If bot is running and obstacle is within 5m, it immediately turns RED

## Technical Details

### Ray-Circle Intersection Math

For a ray from position `(x, y)` in direction `(dx, dy)` and a circle at `(obs_x, obs_y)` with radius `obs_radius`:

```
a = dx² + dy²
b = 2(dx(x - obs_x) + dy(y - obs_y))
c = (x - obs_x)² + (y - obs_y)² - obs_radius²

discriminant = b² - 4ac

if discriminant ≥ 0:
    t₁ = (-b - √discriminant) / (2a)
    t₂ = (-b + √discriminant) / (2a)
    distance = min(positive values of t₁, t₂)
```

### Performance

- LIDAR scans at 1Hz (360 readings per scan)
- Each reading checks all obstacles (O(n) per ray)
- Total: 360 × n obstacle checks per second
- Fast enough for interactive use

## Limitations

1. Small obstacles (30cm) may be missed between LIDAR rays (1° resolution)
2. Color updates happen at 1Hz (LIDAR scan rate)
3. Obstacles exactly at 5m may flicker due to floating-point precision
4. Does not account for partial occlusion (if obstacle A blocks obstacle B)

## Future Enhancements

- [ ] Add partial transparency for partially visible obstacles
- [ ] Show LIDAR rays as lines to detected obstacles
- [ ] Add distance labels on detected obstacles
- [ ] Color gradient based on distance (closer = brighter red)
- [ ] Occlusion handling (obstacles behind other obstacles)
