"""
ASYNC SCAN CODE - EXACT LOCATIONS AND EXPLANATIONS
===================================================

This file shows the exact code I wrote for asynchronous scanning,
with line-by-line explanations.
"""

# =============================================================================
# FILE: src/sensors.py
# LINES: 3-5 - Added threading imports
# =============================================================================

from typing import List, Tuple, Optional, Callable  # Added Optional, Callable
import time
import threading  # ← NEW: For background threads
from dataclasses import dataclass


# =============================================================================
# FILE: src/sensors.py  
# LINES: 44-51 - Added threading state variables in __init__
# =============================================================================

def __init__(self, scan_frequency: float = 1.0, resolution: int = 360, max_range: float = 5.0):
    # ... existing code ...
    
    # ↓↓↓ NEW: Continuous scanning support ↓↓↓
    self._scan_thread = None                    # Thread object for background scanning
    self._stop_continuous_scan = threading.Event()  # Event flag to stop thread
    self._latest_scan = None                    # Stores most recent scan data
    self._scan_lock = threading.Lock()          # Mutex for thread-safe access
    self._scan_callback = None                  # User's callback function
    self._scan_count = 0                        # Counter for total scans


# =============================================================================
# FILE: src/sensors.py
# LINES: 65-84 - Created start_continuous_scan() method
# =============================================================================

def start_continuous_scan(self, callback: Optional[Callable[[List[LidarReading]], None]] = None) -> None:
    """
    ← NEW METHOD ←
    Start continuous asynchronous LIDAR scanning in background thread.
    
    Args:
        callback: Optional callback function called after each scan with scan data
    """
    # Check if already running
    if self._scan_thread and self._scan_thread.is_alive():
        print("LIDAR: Continuous scan already running")
        return
    
    # Save callback and reset state
    self._scan_callback = callback              # Store user's callback
    self._stop_continuous_scan.clear()          # Clear stop signal (flag DOWN)
    self._is_scanning = True                    # Mark as scanning
    self._scan_count = 0                        # Reset counter
    
    # Create and start background thread
    self._scan_thread = threading.Thread(
        target=self._continuous_scan_loop,      # ← Function to run in thread
        daemon=True                             # ← Auto-die when main exits
    )
    self._scan_thread.start()                   # ← START THE THREAD!
    print(f"LIDAR: Started continuous scanning at {self.scan_frequency}Hz")


# =============================================================================
# FILE: src/sensors.py
# LINES: 86-94 - Created stop_continuous_scan() method
# =============================================================================

def stop_continuous_scan(self) -> None:
    """← NEW METHOD ← Stop continuous LIDAR scanning."""
    if not self._scan_thread or not self._scan_thread.is_alive():
        return  # Nothing to stop
    
    self._stop_continuous_scan.set()            # ← Raise stop signal (flag UP)
    self._scan_thread.join(timeout=2.0)         # ← Wait for thread to finish
    self._scan_thread = None                    # ← Clean up
    print(f"LIDAR: Stopped continuous scanning (completed {self._scan_count} scans)")


# =============================================================================
# FILE: src/sensors.py
# LINES: 96-121 - Created _continuous_scan_loop() - THE HEART OF ASYNC SCANNING
# =============================================================================

def _continuous_scan_loop(self) -> None:
    """← NEW METHOD ← Background thread loop for continuous scanning."""
    
    # ↓↓↓ THIS RUNS IN THE BACKGROUND THREAD ↓↓↓
    while not self._stop_continuous_scan.is_set():  # Loop until stop signal
        
        scan_start = time.time()                # Record start time
        
        # ═══ STEP 1: Perform the scan ═══
        scan_data = self.get_scan()             # Get 360 LIDAR readings
        self._scan_count += 1                   # Increment counter
        
        # ═══ STEP 2: Store scan data (THREAD-SAFE) ═══
        with self._scan_lock:                   # ← LOCK (prevent race conditions)
            self._latest_scan = scan_data       # Store for main thread
        # Lock auto-released here
        
        # ═══ STEP 3: Call user's callback ═══
        if self._scan_callback:
            try:
                self._scan_callback(scan_data)  # ← User gets notified!
            except Exception as e:
                print(f"LIDAR: Error in scan callback: {e}")
        
        # ═══ STEP 4: Wait for next scan period ═══
        elapsed = time.time() - scan_start      # How long did scan take?
        sleep_time = max(0, self.scan_period - elapsed)  # Time to wait
        
        if sleep_time > 0:
            # Sleep but wake up if stop signal is raised
            self._stop_continuous_scan.wait(sleep_time)


# =============================================================================
# FILE: src/sensors.py
# LINES: 123-130 - Created get_latest_scan() method
# =============================================================================

def get_latest_scan(self) -> Optional[List[LidarReading]]:
    """
    ← NEW METHOD ←
    Get the most recent scan from continuous scanning.
    
    Returns:
        Latest scan data or None if no scan available
    """
    with self._scan_lock:                       # ← LOCK (thread-safe read)
        return self._latest_scan
    # Lock auto-released here


# =============================================================================
# FILE: src/bot.py
# LINES: 3 - Added Callable import
# =============================================================================

from typing import List, Optional, Callable  # ← Added Callable


# =============================================================================
# FILE: src/bot.py
# LINES: 85-105 - Created bot.start() method
# =============================================================================

def start(self, lidar_callback: Optional[Callable[[List[LidarReading]], None]] = None) -> None:
    """
    ← NEW METHOD ←
    Start the bot with continuous LIDAR scanning.
    
    Args:
        lidar_callback: Optional callback function called after each LIDAR scan
    """
    if not self._initialized:
        raise RuntimeError("Bot not initialized. Call initialize() first.")
    
    if self._running:
        print("Bot: Already running")
        return
    
    # Update LIDAR with position
    if self.position and self.environment_bounds:
        self.lidar.set_environment_context(self.position, self.environment_bounds)
    
    # ↓↓↓ START CONTINUOUS SCANNING ↓↓↓
    self.lidar.start_continuous_scan(callback=lidar_callback)
    
    self._running = True
    print("Bot: Started with continuous LIDAR scanning")


# =============================================================================
# FILE: src/bot.py
# LINES: 107-121 - Created bot.stop() method
# =============================================================================

def stop(self) -> None:
    """← NEW METHOD ← Stop the bot and continuous scanning."""
    if not self._running:
        print("Bot: Already stopped")
        return
    
    # ↓↓↓ STOP CONTINUOUS SCANNING ↓↓↓
    self.lidar.stop_continuous_scan()           # ← Stops background thread
    
    # Stop motors
    self.motors.stop_all()
    
    self._running = False
    print("Bot: Stopped")


# =============================================================================
# FILE: src/bot.py
# LINES: 123-130 - Created bot.get_latest_lidar_scan() method
# =============================================================================

def get_latest_lidar_scan(self) -> Optional[List[LidarReading]]:
    """
    ← NEW METHOD ←
    Get the most recent LIDAR scan from continuous scanning.
    
    Returns:
        Latest scan data or None if no scan available
    """
    return self.lidar.get_latest_scan()         # ← Thread-safe access


# =============================================================================
# SUMMARY OF ALL NEW CODE
# =============================================================================

"""
FILES MODIFIED:
1. src/sensors.py
   - Added: import threading
   - Added: 6 instance variables for threading
   - Added: start_continuous_scan() method (19 lines)
   - Added: stop_continuous_scan() method (9 lines)
   - Added: _continuous_scan_loop() method (26 lines)
   - Added: get_latest_scan() method (8 lines)
   
2. src/bot.py
   - Added: import Callable
   - Added: start() method (20 lines)
   - Added: stop() method (15 lines)
   - Added: get_latest_lidar_scan() method (8 lines)

TOTAL NEW CODE: ~105 lines

KEY THREADING CONCEPTS USED:
1. threading.Thread - Create background thread
2. threading.Event - Signal to stop thread
3. threading.Lock - Prevent race conditions
4. daemon=True - Auto-terminate thread
5. with lock: - Context manager for safe access
"""

print(__doc__)
