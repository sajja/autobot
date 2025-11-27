# Interactive Bot Control Guide

## Overview

The autonomous bot now features an interactive GUI with a "Start Bot" button that triggers LIDAR scanning.

## LIDAR Configuration

- **Frequency**: 1 Hz (1 scan per second)
- **Resolution**: 360 points per scan (1° increments)
- **Data Output**: Angle, Distance, Intensity

## LIDAR Output Format

Each scan produces 360 readings with the following format:

```
Angle (°)   Distance (m)   Intensity
0           1.20           120
1           1.19           118
2           1.22           125
...
359         1.15           110
```

### Data Fields:
- **Angle**: 0-359 degrees (integer)
- **Distance**: Range in meters (float, typically 0.5-5.0m)
- **Intensity**: Signal strength (integer, 0-255)

## Usage

### Quick Start

```bash
# Run the interactive demo
python3 examples/simple_interactive.py
```

### Steps:
1. GUI window opens showing the environment
2. Bot is displayed as a blue circle with direction arrow
3. Click the **"Start Bot"** button
4. LIDAR scan starts and results appear in the console
5. View the scan data table
6. Close window when done

### Programmatic Usage

```python
from src.environment import Environment
from src.bot import Bot

# Create environment and bot
env = Environment(width=10.0, height=10.0)
bot = Bot(lidar_frequency=1.0)  # 1Hz LIDAR

# Place bot
env.set_bot_position(x=5.0, y=5.0, orientation=0.0)

# Show interactive GUI
env.visualize_interactive(bot_instance=bot)
```

### Manual LIDAR Control

```python
from src.bot import Bot

# Create bot
bot = Bot(lidar_frequency=1.0)
bot.initialize()

# Get a scan
scan_data = bot.get_lidar_scan()

# Print results
for reading in scan_data[:10]:  # First 10 points
    print(f"Angle: {reading.angle}°, "
          f"Distance: {reading.distance:.2f}m, "
          f"Intensity: {reading.intensity}")
```

### Saving Scan Data

```python
from src.lidar_utils import save_lidar_scan_csv

# After getting scan data
save_lidar_scan_csv(scan_data, "scan_output.csv")
```

## Example Output

When you click "Start Bot", you'll see:

```
============================================================
START BOT BUTTON CLICKED!
============================================================
Bot: Initializing systems...
LIDAR: Started scanning at 1.0Hz
...

--- Starting LIDAR Scan ---

LIDAR Scan Results (Total: 360 readings)
Scan Frequency: 1.0 Hz
------------------------------------------------------------
   Angle (°)    Distance (m)       Intensity
------------------------------------------------------------
           0            1.24             112
           1            1.22             123
           2            1.15             115
...
         359            1.18             122
------------------------------------------------------------
Scan completed at 1764259536.09
```

## Customization

### Change LIDAR Frequency

```python
# Create bot with different frequency (e.g., 5Hz)
bot = Bot(lidar_frequency=5.0)
```

### Custom Callback

```python
def my_callback(bot_instance, scan_data):
    print(f"Custom processing: {len(scan_data)} points received")
    # Your custom processing here

env.visualize_interactive(bot_instance=bot, on_start_callback=my_callback)
```

## Files

- `src/environment.py` - Environment with interactive GUI
- `src/bot.py` - Bot class with LIDAR control
- `src/sensors.py` - LIDAR sensor implementation
- `src/lidar_utils.py` - Utility functions for LIDAR data
- `examples/simple_interactive.py` - Simple demo
- `examples/interactive_bot.py` - Full demo with instructions

## Features

✅ Interactive GUI with button control  
✅ 1Hz LIDAR scanning (configurable)  
✅ 360-degree coverage (360 data points)  
✅ Distance and intensity measurements  
✅ Console output of scan data  
✅ Real-time status updates in GUI  
✅ CSV export capability  

## Next Steps

- Add obstacle detection from LIDAR data
- Implement mapping from scans
- Add path planning based on LIDAR
- Create continuous scanning mode
- Add LIDAR visualization on the GUI
