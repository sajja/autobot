"""
LIVE DEMONSTRATION - Asynchronous LIDAR Scanning
Watch the background thread work in real-time!
"""

from src.environment import Environment
from src.bot import Bot
import time


def demo_async_scanning():
    """Live demo showing async scanning in action."""
    
    print("="*70)
    print("ASYNCHRONOUS LIDAR SCANNING - LIVE DEMO")
    print("="*70)
    print()
    
    # Setup
    env = Environment(width=25.0, height=25.0)
    bot = Bot(lidar_frequency=2.0)  # 2Hz = 2 scans per second
    env.set_bot_position(x=2.0, y=2.0, orientation=0.0)
    bot.position = (2.0, 2.0)
    bot.environment_bounds = (25.0, 25.0)
    bot.initialize()
    
    print("Setup:")
    print("  • Bot at position (2.0, 2.0)")
    print("  • LIDAR frequency: 2Hz (2 scans/second)")
    print("  • Scan period: 0.5 seconds")
    print()
    
    # Define callback to show what happens in background thread
    scan_times = []
    
    def background_callback(scan_data):
        """This runs IN THE BACKGROUND THREAD!"""
        scan_times.append(time.time())
        scan_num = len(scan_times)
        detected = sum(1 for r in scan_data if r.distance > 0)
        
        print(f"  🔄 [Background Thread] Scan #{scan_num} completed!")
        print(f"     - Time: {time.time():.3f}")
        print(f"     - Detected: {detected}/360 points")
        print(f"     - Thread ID: {threading.current_thread().name}")
        print()
    
    import threading
    
    # Show main thread info
    print(f"Main Thread ID: {threading.current_thread().name}")
    print()
    
    # Start continuous scanning
    print("▶️  STARTING continuous scan...")
    print(f"   Background thread will scan every 0.5 seconds")
    print()
    
    bot.start(lidar_callback=background_callback)
    
    # Main thread continues doing other things!
    print("🔵 Main thread is FREE! Doing other work...")
    print()
    
    for i in range(4):
        print(f"  [Main Thread] Working on task {i+1}...")
        time.sleep(0.3)  # Main thread does work
        
        # Access latest scan while background thread keeps scanning
        latest = bot.get_latest_lidar_scan()
        if latest:
            print(f"  [Main Thread] Checked latest scan: {len(latest)} readings")
        print()
    
    print("⏸️  Main thread sleeping for 2 seconds...")
    print("   (Background thread keeps scanning!)")
    print()
    time.sleep(2)
    
    # Stop scanning
    print("⏹️  STOPPING continuous scan...")
    bot.stop()
    
    # Analysis
    print()
    print("="*70)
    print("ANALYSIS:")
    print("="*70)
    print(f"Total scans: {len(scan_times)}")
    print(f"Expected: ~{int(3.2 * 2)} scans (3.2 seconds × 2Hz)")
    print()
    
    if len(scan_times) > 1:
        print("Scan intervals:")
        for i in range(1, len(scan_times)):
            interval = scan_times[i] - scan_times[i-1]
            print(f"  Scan {i} → {i+1}: {interval:.3f}s (expected: 0.500s)")
    
    print()
    print("✅ KEY OBSERVATIONS:")
    print("   1. Background thread scans independently")
    print("   2. Main thread continues other work")
    print("   3. Both threads run simultaneously")
    print("   4. Scan timing is consistent (~0.5s intervals)")
    print("   5. Thread-safe data access with locks")
    
    bot.shutdown()
    print()
    print("="*70)
    print("Demo complete!")
    print("="*70)


if __name__ == "__main__":
    demo_async_scanning()
