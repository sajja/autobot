"""
ASYNCHRONOUS LIDAR SCANNING - CODE EXPLANATION
==============================================

This demonstrates how the asynchronous scanning works with code examples.
"""

# ============================================================================
# 1. INITIALIZATION - Setting up threading components
# ============================================================================

def __init__(self, scan_frequency: float = 1.0, ...):
    """Initialize LIDAR with threading components."""
    
    # Basic LIDAR settings
    self.scan_frequency = scan_frequency  # e.g., 1.0 Hz = 1 scan/second
    self.scan_period = 1.0 / scan_frequency  # e.g., 1.0 seconds per scan
    
    # Threading components
    self._scan_thread = None                    # The background thread object
    self._stop_continuous_scan = threading.Event()  # Signal to stop the thread
    self._latest_scan = None                    # Stores most recent scan data
    self._scan_lock = threading.Lock()          # Protects _latest_scan from race conditions
    self._scan_callback = None                  # User's callback function
    self._scan_count = 0                        # Counts total scans


# ============================================================================
# 2. STARTING CONTINUOUS SCAN - Launching the background thread
# ============================================================================

def start_continuous_scan(self, callback=None):
    """Start background thread that scans continuously."""
    
    # Save the user's callback function (called after each scan)
    self._scan_callback = callback
    
    # Clear the stop signal (Event is like a flag)
    self._stop_continuous_scan.clear()  # Flag is DOWN = "keep running"
    
    # Reset scan counter
    self._scan_count = 0
    
    # Create and start background thread
    # daemon=True means thread auto-dies when main program exits
    self._scan_thread = threading.Thread(
        target=self._continuous_scan_loop,  # Function to run in thread
        daemon=True                         # Auto-terminate with main program
    )
    self._scan_thread.start()  # START THE THREAD! 🚀


# ============================================================================
# 3. THE BACKGROUND LOOP - This runs in the separate thread
# ============================================================================

def _continuous_scan_loop(self):
    """This function runs in the background thread continuously."""
    
    # Keep looping until stop signal is set
    while not self._stop_continuous_scan.is_set():  # Check if flag is DOWN
        
        # --- STEP 1: Record start time ---
        scan_start = time.time()
        
        # --- STEP 2: Perform the actual 360° LIDAR scan ---
        scan_data = self.get_scan()  # Returns List[LidarReading] with 360 points
        self._scan_count += 1
        
        # --- STEP 3: Store scan data (THREAD-SAFE) ---
        with self._scan_lock:  # LOCK: Only one thread can access at a time
            self._latest_scan = scan_data
        # Lock automatically released here
        
        # --- STEP 4: Call user's callback function (if provided) ---
        if self._scan_callback:
            try:
                self._scan_callback(scan_data)  # User gets notified!
            except Exception as e:
                print(f"LIDAR: Error in scan callback: {e}")
        
        # --- STEP 5: Wait for next scan period ---
        elapsed = time.time() - scan_start  # How long did scan take?
        sleep_time = max(0, self.scan_period - elapsed)  # Time left to wait
        
        if sleep_time > 0:
            # Sleep but check stop signal every interval
            # If stop signal raised, wake up immediately!
            self._stop_continuous_scan.wait(sleep_time)


# ============================================================================
# 4. GETTING LATEST SCAN - Main thread accesses scan data (THREAD-SAFE)
# ============================================================================

def get_latest_scan(self):
    """Retrieve the most recent scan (called from main thread)."""
    
    # Use lock to safely read data
    with self._scan_lock:  # LOCK: Prevent reading while background thread is writing
        return self._latest_scan
    # Lock released here


# ============================================================================
# 5. STOPPING CONTINUOUS SCAN - Clean shutdown of background thread
# ============================================================================

def stop_continuous_scan(self):
    """Stop the background scanning thread."""
    
    if not self._scan_thread or not self._scan_thread.is_alive():
        return  # Thread not running, nothing to stop
    
    # Raise the stop signal (Event flag goes UP)
    self._stop_continuous_scan.set()  # Flag is UP = "stop running"
    
    # Wait for thread to finish (max 2 seconds)
    self._scan_thread.join(timeout=2.0)
    
    # Clean up
    self._scan_thread = None
    print(f"LIDAR: Stopped continuous scanning (completed {self._scan_count} scans)")


# ============================================================================
# VISUAL TIMELINE - How it works
# ============================================================================

"""
TIME →

MAIN THREAD:                BACKGROUND THREAD:
    │                              │
    │ bot.start() ─────────────────┤
    │                              │ [Thread starts]
    │                              │
    │                              ├─ scan_start = time.time()
    │                              ├─ scan_data = get_scan()  (360 readings)
    │                              ├─ with lock:
    │                              │    _latest_scan = scan_data
    │                              ├─ callback(scan_data)
    │                              ├─ sleep(0.99s)
    │                              │
    │ latest = bot.get_latest_scan() ─┤
    │ ← returns scan_data          │
    │                              │
    │                              ├─ scan_start = time.time()
    │                              ├─ scan_data = get_scan()  (360 readings)
    │                              ├─ with lock:
    │                              │    _latest_scan = scan_data
    │                              ├─ callback(scan_data)
    │                              ├─ sleep(0.99s)
    │                              │
    │ bot.stop() ──────────────────┤
    │                              ├─ [Stop signal raised]
    │                              └─ [Thread exits loop]
    │                              
    └─ Thread cleaned up
"""


# ============================================================================
# KEY CONCEPTS
# ============================================================================

"""
1. THREADING.THREAD
   - Creates a new thread of execution
   - daemon=True means it dies when main program exits
   - target= specifies the function to run in that thread

2. THREADING.EVENT
   - A simple flag that can be set() or clear()
   - is_set() checks if flag is raised
   - wait(timeout) sleeps but can be interrupted when flag is set

3. THREADING.LOCK
   - Ensures only one thread accesses data at a time
   - Prevents "race conditions" where threads interfere
   - "with lock:" automatically acquires and releases

4. CALLBACK FUNCTION
   - User provides function: def callback(scan_data): ...
   - Called automatically after each scan
   - Runs IN THE BACKGROUND THREAD (not main thread)
"""


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

"""
# Define callback
def my_callback(scan_data):
    print(f"Got {len(scan_data)} readings!")

# Start scanning
lidar.start_continuous_scan(callback=my_callback)

# Background thread now runs:
#   Loop:
#     1. Scan (takes ~0.01s)
#     2. Store in _latest_scan
#     3. Call my_callback(scan_data)  ← "Got 360 readings!" printed
#     4. Sleep ~0.99s
#     5. Repeat

# Main thread can access latest scan anytime
latest = lidar.get_latest_scan()

# Stop when done
lidar.stop_continuous_scan()
"""


# ============================================================================
# THREAD SAFETY EXAMPLE
# ============================================================================

"""
WITHOUT LOCK (DANGEROUS):
    Background Thread         Main Thread
         │                        │
         ├─ _latest_scan = [1,2,3,...]
         │                        ├─ data = _latest_scan
         ├─ _latest_scan = [4,5,6,...]
         │                        └─ print(data)  ← Could be corrupted!
         
WITH LOCK (SAFE):
    Background Thread         Main Thread
         │                        │
         ├─ with lock:            │
         │    _latest_scan = [1,2,3,...]
         │                        ├─ with lock:  [BLOCKED, waiting for lock]
         └─ [lock released]       │
                                  ├─ data = _latest_scan
                                  └─ [lock released]
                                  
The lock ensures only ONE thread accesses _latest_scan at a time!
"""


# ============================================================================
# TIMING ANALYSIS
# ============================================================================

"""
At 1Hz (1 scan per second):

Time 0.00s:  scan_start = 0.00
             get_scan() ────────────── [takes ~0.01s]
Time 0.01s:  with lock: store data ── [takes ~0.0001s]
             callback() ─────────────── [user defined, ~0.001s]
Time 0.012s: elapsed = 0.012s
             sleep_time = 1.0 - 0.012 = 0.988s
             sleep(0.988s) ────────────
Time 1.00s:  [Loop repeats]

Result: Scan happens at 0s, 1s, 2s, 3s... (exactly 1Hz!)
"""

print(__doc__)
