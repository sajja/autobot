# Autonomous Vehicle Bot

An autonomous vehicle simulation with LIDAR sensors, sonar, and motor control, featuring an interactive GUI for real-time control and visualization.

## Features

🤖 **Autonomous Bot**
- 4 stepper motors for mobility
- Rotating LIDAR sensor (configurable frequency, default 1Hz)
- Sonar sensor for obstacle detection
- 360-degree scanning capability

🗺️ **Environment Simulation**
- Grid-based environment (customizable size)
- GUI visualization with matplotlib
- Interactive controls with button interface
- **Keyboard controls** for manual bot movement (arrow keys)
- Obstacle support with collision detection
- Wall detection with RED dot visualization

📡 **LIDAR Scanning**
- Angle: 0-359° (360 data points)
- Distance measurements in meters
- Intensity values (0-255)
- Real-time scan output
- CSV export capability

## Project Structure

```
bot/
├── src/
│   ├── bot.py              # Main bot class
│   ├── environment.py      # Environment & visualization
│   ├── sensors.py          # LIDAR and sonar sensors
│   ├── motors.py           # Stepper motor control
│   ├── lidar_utils.py      # LIDAR data utilities
│   └── main.py             # Demo application
├── examples/
│   ├── keyboard_control_demo.py  # Keyboard control demo
│   ├── wall_detection_demo.py    # Wall detection visualization
│   ├── simple_interactive.py     # Interactive GUI demo
│   └── simple_gui.py             # Basic GUI example
├── tests/                  # Test files
├── docs/
│   ├── KEYBOARD_CONTROLS.md      # Keyboard control guide
│   ├── RED_DOTS_WALL_DETECTION.md  # Wall detection guide
│   └── INTERACTIVE_GUIDE.md      # Interactive feature guide
├── requirements.txt        # Dependencies
└── README.md              # This file
```

## Quick Start

### Prerequisites

- Python 3.8 or higher
- matplotlib
- numpy

### Installation

On Ubuntu/Debian:
```bash
sudo apt-get install python3-matplotlib python3-numpy
```

Or use pip (in virtual environment):
```bash
pip install -r requirements.txt
```

### Run Interactive Demo

**Basic Interactive Demo:**
```bash
python3 examples/simple_interactive.py
```

**Keyboard Control Demo (Recommended):**
```bash
python3 examples/keyboard_control_demo.py
```

**Instructions:**
1. GUI window opens with environment visualization
2. Bot appears as blue circle with direction arrow
3. Click **"Start Bot"** button (turns GREEN, bot turns BLUE)
4. **Use arrow keys to control the bot:**
   - ⬆️ UP: Move forward
   - ⬇️ DOWN: Move backward
   - ⬅️ LEFT: Rotate counter-clockwise
   - ➡️ RIGHT: Rotate clockwise
5. LIDAR continuously scans and outputs data to console
6. Navigate to corners to see wall detection (RED dots)
7. Add obstacles with "Place Object" button

### Run Basic Bot Demo

```bash
python -m src.main
```

## Usage Examples

### Interactive GUI Control

```python
from src.environment import Environment
from src.bot import Bot

# Create environment and bot
env = Environment(width=10.0, height=10.0)
bot = Bot(lidar_frequency=1.0)  # 1Hz LIDAR

# Place bot in environment
env.set_bot_position(x=5.0, y=5.0, orientation=0.0)

# Open interactive GUI with Start button
env.visualize_interactive(bot_instance=bot)
```

### Manual LIDAR Scanning

```python
from src.bot import Bot

# Create and initialize bot
bot = Bot(lidar_frequency=1.0)
bot.initialize()

# Get LIDAR scan
scan_data = bot.get_lidar_scan()

# Process scan data
for reading in scan_data:
    print(f"Angle: {reading.angle}°, "
          f"Distance: {reading.distance:.2f}m, "
          f"Intensity: {reading.intensity}")
```

### Environment Visualization

```python
from src.environment import Environment

env = Environment(width=10.0, height=10.0)
env.set_bot_position(x=5.0, y=5.0, orientation=45.0)

# Static visualization
env.visualize(show=True)

# Or save to file
env.visualize(show=False, save_path="environment.png")
```

## LIDAR Output Format

Each scan produces 360 readings:

```
Angle (°)   Distance (m)   Intensity
0           1.20           120
1           1.19           118
2           1.22           125
...
359         1.15           110
```

- **Angle**: 0-359° (1° increments)
- **Distance**: Range in meters
- **Intensity**: Signal strength (0-255)

## Documentation

- [Keyboard Controls Guide](docs/KEYBOARD_CONTROLS.md) - Complete keyboard control documentation
- [Keyboard Quick Reference](KEYBOARD_QUICK_REFERENCE.md) - Quick reference for arrow keys
- [Wall Detection Guide](docs/RED_DOTS_WALL_DETECTION.md) - Wall detection visualization
- [Interactive Features](docs/INTERACTIVE_GUIDE.md) - Interactive GUI features

## Running Tests

```bash
pytest tests/
```

## Development

To install the project in editable mode for development:

```bash
pip install -e .
```

## License

This project is licensed under the MIT License.
