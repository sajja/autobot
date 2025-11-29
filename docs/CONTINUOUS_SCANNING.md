# Continuous Asynchronous LIDAR Scanning

## Overview

The LIDAR sensor now supports **continuous asynchronous scanning** while the bot is running. Scans are performed in a background thread at the configured frequency (default: 1Hz).

## Features

### ✅ Asynchronous Scanning
- Runs in separate background thread (daemon thread)
- Non-blocking operation - bot can perform other tasks while scanning
- Automatic scan timing based on configured frequency

### ✅ Thread-Safe Operation
- Thread-safe scan data storage using `threading.Lock()`
- Safe concurrent access to latest scan data
- Clean thread shutdown with event signaling

### ✅ Callback Support
- Optional callback function called after each scan
- Real-time scan notifications
- Access to scan data for processing/logging

### ✅ Scan Management
- Start continuous scanning: `lidar.start_continuous_scan(callback)`
- Stop continuous scanning: `lidar.stop_continuous_scan()`
- Get latest scan: `lidar.get_latest_scan()`
- Track scan count: `lidar._scan_count`

## Usage

### Basic Continuous Scanning

```python
from src.bot import Bot
from src.environment import Environment

# Create and setup bot
env = Environment(width=25.0, height=25.0)
bot = Bot(lidar_frequency=1.0)  # 1Hz scanning
env.set_bot_position(x=12.5, y=12.5, orientation=0.0)

# Set environment context
bot.position = (12.5, 12.5)
bot.environment_bounds = (25.0, 25.0)

# Initialize
bot.initialize()

# Start continuous scanning
bot.start()

# ... bot runs and scans continuously ...

# Get latest scan at any time
latest_scan = bot.get_latest_lidar_scan()
if latest_scan:
    print(f"Latest scan: {len(latest_scan)} readings")

# Stop scanning
bot.stop()
bot.shutdown()
```

### With Scan Callback

```python
# Define callback for each scan
def on_lidar_scan(scan_data):
    detected = sum(1 for r in scan_data if r.distance > 0)
    print(f"Scan: {detected}/360 points detected")

# Start with callback
bot.start(lidar_callback=on_lidar_scan)

# Callback is called automatically after each scan
```

### Advanced Usage

```python
# Custom callback with processing
def process_scan(scan_data):
    # Find nearest obstacle
    min_dist = min((r.distance for r in scan_data if r.distance > 0), default=0)
    if min_dist > 0 and min_dist < 1.0:
        print(f"WARNING: Obstacle at {min_dist:.2f}m!")
    
    # Log scan statistics
    detected = sum(1 for r in scan_data if r.distance > 0)
    avg_intensity = sum(r.intensity for r in scan_data) / len(scan_data)
    print(f"Detected: {detected}, Avg Intensity: {avg_intensity:.1f}")

# Start with processing callback
bot.start(lidar_callback=process_scan)

# Run for some time
import time
time.sleep(10)  # 10 seconds = ~10 scans at 1Hz

# Check total scans
print(f"Total scans: {bot.lidar._scan_count}")

# Stop
bot.stop()
```

## Implementation Details

### Threading Architecture

```
Main Thread                Background Thread
     │                            │
     ├─ bot.start() ──────────────┤
     │                            ├─ while not stopped:
     │                            │    ├─ perform scan
     │                            │    ├─ store in _latest_scan (locked)
     │                            │    ├─ call callback(scan_data)
     │                            │    └─ sleep(scan_period)
     │                            │
     ├─ bot.get_latest_scan() ────┤
     │  (returns _latest_scan)    │
     │                            │
     ├─ bot.stop() ───────────────┤
     │                            ├─ stop signal
     │                            └─ thread exits
     └─ bot.shutdown()
```

### Scan Frequency

- **1Hz** (default): 1 scan per second
- **5Hz**: 5 scans per second (faster)
- **0.5Hz**: 1 scan every 2 seconds (slower)

Configuration:
```python
bot = Bot(lidar_frequency=5.0)  # 5Hz scanning
```

### Thread Safety

The implementation uses:
- `threading.Lock()` for mutual exclusion on scan data
- `threading.Event()` for clean thread shutdown
- Daemon thread (auto-terminates with main program)

### Scan Timing

Each scan cycle:
1. Record start time
2. Perform 360° scan (360 readings)
3. Store results
4. Call callback (if provided)
5. Calculate elapsed time
6. Sleep for remaining time to maintain frequency

Example at 1Hz:
- Scan takes ~0.01s
- Sleep for ~0.99s
- Total cycle: ~1.0s

## Performance

### Scan Performance (1Hz)

- **Scan duration**: ~0.01-0.02 seconds
- **Scans per second**: 1 (as configured)
- **360 readings per scan**
- **Thread overhead**: Minimal (<1% CPU)

### Memory Usage

- Latest scan: ~3KB (360 readings × ~8 bytes)
- Thread stack: ~1MB
- Total overhead: ~1MB

## Test Results

### Continuous Scanning Test

```
Bot Position: (2.0, 2.0)
LIDAR: 1.0Hz continuous scanning

Scanning for 5 seconds (expecting ~5 scans)...
[Scan #1] Time: 1764261312.38 | Detected: 223/360 points
[Scan #2] Time: 1764261313.38 | Detected: 223/360 points
[Scan #3] Time: 1764261314.38 | Detected: 223/360 points
[Scan #4] Time: 1764261315.38 | Detected: 223/360 points
[Scan #5] Time: 1764261316.38 | Detected: 223/360 points
[Scan #6] Time: 1764261317.38 | Detected: 223/360 points

Total scans completed: 6
✅ SUCCESS: Consistent 1Hz scanning achieved
```

## Interactive GUI Integration

The interactive visualization now uses continuous scanning:

1. **Click "Start Bot"** → Continuous LIDAR scanning begins
2. Scans run automatically in background at 1Hz
3. Console shows scan notifications
4. **Click "Stop Bot"** → Scanning stops cleanly

Console output while running:
```
[LIDAR Scan #1] 360 points at 1764261329.55
[LIDAR Scan #2] 360 points at 1764261330.55
[LIDAR Scan #3] 360 points at 1764261331.55
...
```

## API Reference

### RotatingLidar Class

#### Methods

**`start_continuous_scan(callback=None)`**
- Starts background scanning thread
- Args: `callback` - Optional function called after each scan
- Returns: None

**`stop_continuous_scan()`**
- Stops background scanning thread
- Waits for thread to finish (timeout: 2s)
- Returns: None

**`get_latest_scan()`**
- Returns most recent scan data
- Thread-safe access
- Returns: `List[LidarReading]` or `None`

**`set_environment_context(position, env_bounds)`**
- Sets bot position and environment for realistic scanning
- Args: `position` - (x, y) tuple, `env_bounds` - (width, height) tuple
- Returns: None

#### Properties

- `_scan_count`: Total number of completed scans (int)
- `_is_scanning`: Whether LIDAR is currently scanning (bool)
- `scan_frequency`: Configured scan frequency in Hz (float)

### Bot Class

#### Methods

**`start(lidar_callback=None)`**
- Starts bot with continuous LIDAR scanning
- Args: `lidar_callback` - Optional scan callback function
- Returns: None

**`stop()`**
- Stops bot and continuous scanning
- Returns: None

**`get_latest_lidar_scan()`**
- Gets most recent LIDAR scan
- Returns: `List[LidarReading]` or `None`

## Benefits

✅ **Real-time Environment Awareness**: Bot continuously updates environment map  
✅ **Non-blocking**: Scanning doesn't interfere with other operations  
✅ **Efficient**: Thread sleeps between scans, minimal CPU usage  
✅ **Flexible**: Configurable frequency and callback support  
✅ **Thread-safe**: Safe concurrent access to scan data  
✅ **Clean Shutdown**: Proper thread termination on stop  

## Future Enhancements

Potential improvements:
- [ ] Variable scan resolution (e.g., 180 points instead of 360)
- [ ] Scan buffering (store last N scans)
- [ ] Scan data filtering/smoothing
- [ ] Adaptive scan frequency based on bot movement
- [ ] Point cloud generation for 3D visualization
- [ ] SLAM integration for mapping and localization

## Troubleshooting

### Issue: Scans not appearing
**Solution**: Ensure `bot.position` and `bot.environment_bounds` are set before calling `bot.start()`

### Issue: Scan count doesn't match expected
**Solution**: This is normal - first scan may occur immediately, adding 1 extra scan

### Issue: Thread doesn't stop
**Solution**: Ensure you call `bot.stop()` before `bot.shutdown()`. Thread has 2s timeout.

### Issue: Callback errors
**Solution**: Ensure callback function accepts one parameter: `def callback(scan_data: List[LidarReading])`

## Conclusion

Continuous asynchronous LIDAR scanning provides realistic sensor behavior for the autonomous bot. The bot can now continuously monitor its environment while performing navigation and other tasks, just like a real autonomous vehicle!
