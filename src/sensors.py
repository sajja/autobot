"""Sensor classes for the autonomous vehicle."""

from typing import List, Tuple, Optional, Callable
import time
import threading
from dataclasses import dataclass


@dataclass
class LidarReading:
    """Represents a single LIDAR reading."""
    
    angle: float  # Angle in degrees (0-360)
    distance: float  # Distance in meters
    intensity: int  # Signal intensity (0-255)
    timestamp: float  # Timestamp of the reading


class RotatingLidar:
    """
    Rotating LIDAR sensor for 360-degree mapping.
    Maximum range: 5 meters.
    Scans at configurable frequency (default: 1Hz).
    """
    
    def __init__(self, scan_frequency: float = 1.0, resolution: int = 360, max_range: float = 5.0):
        """
        Initialize the LIDAR sensor.
        
        Args:
            scan_frequency: Scanning frequency in Hz (default: 1Hz)
            resolution: Number of points per 360-degree scan (default: 360)
            max_range: Maximum detection range in meters (default: 5.0m)
        """
        self.scan_frequency = scan_frequency
        self.resolution = resolution
        self.max_range = max_range
        self.scan_period = 1.0 / scan_frequency
        self._is_scanning = False
        self._current_angle = 0.0
        
        # Environment context (set by bot/environment)
        self.position = None  # (x, y) tuple
        self.environment_bounds = None  # (width, height) tuple
        self.obstacles = []  # List of obstacles in environment
        
        # Continuous scanning support
        self._scan_thread = None
        self._stop_continuous_scan = threading.Event()
        self._latest_scan = None
        self._scan_lock = threading.Lock()
        self._scan_callback = None
        self._scan_count = 0
    
    def start_scanning(self) -> None:
        """Start the LIDAR scanning process."""
        self._is_scanning = True
        print(f"LIDAR: Started scanning at {self.scan_frequency}Hz")
    
    def stop_scanning(self) -> None:
        """Stop the LIDAR scanning process."""
        self._is_scanning = False
        self.stop_continuous_scan()
        print("LIDAR: Stopped scanning")
    
    def start_continuous_scan(self, callback: Optional[Callable[[List[LidarReading]], None]] = None) -> None:
        """
        Start continuous asynchronous LIDAR scanning in background thread.
        
        Args:
            callback: Optional callback function called after each scan with scan data
        """
        if self._scan_thread and self._scan_thread.is_alive():
            print("LIDAR: Continuous scan already running")
            return
        
        self._scan_callback = callback
        self._stop_continuous_scan.clear()
        self._is_scanning = True
        self._scan_count = 0
        
        self._scan_thread = threading.Thread(target=self._continuous_scan_loop, daemon=True)
        self._scan_thread.start()
        print(f"LIDAR: Started continuous scanning at {self.scan_frequency}Hz")
    
    def stop_continuous_scan(self) -> None:
        """Stop continuous LIDAR scanning."""
        if not self._scan_thread or not self._scan_thread.is_alive():
            return
        
        self._stop_continuous_scan.set()
        self._scan_thread.join(timeout=2.0)
        self._scan_thread = None
        print(f"LIDAR: Stopped continuous scanning (completed {self._scan_count} scans)")
    
    def _continuous_scan_loop(self) -> None:
        """Background thread loop for continuous scanning."""
        while not self._stop_continuous_scan.is_set():
            scan_start = time.time()
            
            # Perform scan
            scan_data = self.get_scan()
            self._scan_count += 1
            
            # Store latest scan
            with self._scan_lock:
                self._latest_scan = scan_data
            
            # Call callback if provided
            if self._scan_callback:
                try:
                    self._scan_callback(scan_data)
                except Exception as e:
                    print(f"LIDAR: Error in scan callback: {e}")
            
            # Wait for next scan period
            elapsed = time.time() - scan_start
            sleep_time = max(0, self.scan_period - elapsed)
            if sleep_time > 0:
                self._stop_continuous_scan.wait(sleep_time)
    
    def get_latest_scan(self) -> Optional[List[LidarReading]]:
        """
        Get the most recent scan from continuous scanning.
        
        Returns:
            Latest scan data or None if no scan available
        """
        with self._scan_lock:
            return self._latest_scan
    
    def get_scan(self) -> List[LidarReading]:
        """
        Get a complete 360-degree scan.
        
        Returns:
            List of LidarReading objects representing the full scan
        """
        if not self._is_scanning:
            raise RuntimeError("LIDAR is not scanning. Call start_scanning() first.")
        
        scan_data = []
        angle_step = 360.0 / self.resolution
        current_time = time.time()
        
        for i in range(self.resolution):
            angle = i * angle_step
            # Placeholder: In real implementation, this would read from actual sensor
            distance, intensity = self._simulate_reading(angle)
            scan_data.append(LidarReading(angle, distance, intensity, current_time))
        
        return scan_data
    
    def _simulate_reading(self, angle: float) -> Tuple[float, int]:
        """
        Simulate a LIDAR reading (placeholder for actual sensor reading).
        Checks both environment boundaries and obstacles.
        
        Args:
            angle: Angle in degrees
            
        Returns:
            Tuple of (distance in meters, intensity 0-255)
        """
        import math
        
        # If no environment context, return 0 (no obstacles, infinite space)
        if self.position is None or self.environment_bounds is None:
            return 0.0, 0
        
        x, y = self.position
        env_width, env_height = self.environment_bounds
        
        # Convert angle to radians
        angle_rad = math.radians(angle)
        
        # Calculate direction vector
        dx = math.cos(angle_rad)
        dy = math.sin(angle_rad)
        
        # Calculate distance to each wall
        distances = []
        
        # Right wall (x = env_width)
        if dx > 0:
            t = (env_width - x) / dx
            distances.append(t)
        
        # Left wall (x = 0)
        if dx < 0:
            t = -x / dx
            distances.append(t)
        
        # Top wall (y = env_height)
        if dy > 0:
            t = (env_height - y) / dy
            distances.append(t)
        
        # Bottom wall (y = 0)
        if dy < 0:
            t = -y / dy
            distances.append(t)
        
        # Check for obstacles (circular obstacles)
        for obstacle in self.obstacles:
            obs_x = obstacle.position.x
            obs_y = obstacle.position.y
            obs_radius = obstacle.radius
            
            # Ray-circle intersection
            # Ray: P = (x, y) + t * (dx, dy)
            # Circle: (P_x - obs_x)^2 + (P_y - obs_y)^2 = obs_radius^2
            
            # Substitute ray into circle equation:
            # (x + t*dx - obs_x)^2 + (y + t*dy - obs_y)^2 = obs_radius^2
            
            # Expand to quadratic: a*t^2 + b*t + c = 0
            a = dx*dx + dy*dy
            b = 2 * (dx*(x - obs_x) + dy*(y - obs_y))
            c = (x - obs_x)**2 + (y - obs_y)**2 - obs_radius**2
            
            discriminant = b*b - 4*a*c
            
            if discriminant >= 0 and a != 0:
                # Ray intersects circle
                sqrt_disc = math.sqrt(discriminant)
                t1 = (-b - sqrt_disc) / (2*a)
                t2 = (-b + sqrt_disc) / (2*a)
                
                # We want the nearest positive intersection
                if t1 > 0:
                    distances.append(t1)
                elif t2 > 0:
                    distances.append(t2)
        
        # Get minimum positive distance (nearest wall or obstacle)
        valid_distances = [d for d in distances if d > 0]
        if not valid_distances:
            return 0.0, 0
        
        distance = min(valid_distances)
        
        # Clamp to max range (LIDAR cannot see beyond max_range)
        if distance > self.max_range:
            distance = 0.0  # No detection beyond max range
            intensity = 0
        else:
            # Intensity decreases with distance
            base_intensity = 200 - int((distance / self.max_range) * 100)
            intensity = max(50, min(255, base_intensity))
        
        return distance, intensity
    
    def set_environment_context(self, position: Tuple[float, float], env_bounds: Tuple[float, float]) -> None:
        """
        Set the environment context for realistic LIDAR simulation.
        
        Args:
            position: Current (x, y) position of the LIDAR sensor
            env_bounds: Environment (width, height) in meters
        """
        self.position = position
        self.environment_bounds = env_bounds
    
    @property
    def is_scanning(self) -> bool:
        """Check if LIDAR is currently scanning."""
        return self._is_scanning


@dataclass
class SonarReading:
    """Represents a sonar sensor reading."""
    
    distance: float  # Distance in meters
    timestamp: float  # Timestamp of the reading


class SonarSensor:
    """
    Sonar sensor for immediate obstacle detection.
    Used for close-range obstacle avoidance.
    """
    
    def __init__(self, max_range: float = 4.0, min_range: float = 0.02):
        """
        Initialize the sonar sensor.
        
        Args:
            max_range: Maximum detection range in meters (default: 4.0m)
            min_range: Minimum detection range in meters (default: 0.02m)
        """
        self.max_range = max_range
        self.min_range = min_range
        self._enabled = False
    
    def enable(self) -> None:
        """Enable the sonar sensor."""
        self._enabled = True
        print("Sonar: Enabled")
    
    def disable(self) -> None:
        """Disable the sonar sensor."""
        self._enabled = False
        print("Sonar: Disabled")
    
    def get_distance(self) -> SonarReading:
        """
        Get the current distance reading from the sonar sensor.
        
        Returns:
            SonarReading object with distance and timestamp
        """
        if not self._enabled:
            raise RuntimeError("Sonar is not enabled. Call enable() first.")
        
        # Placeholder: In real implementation, this would read from actual sensor
        distance = self._read_sensor()
        return SonarReading(distance, time.time())
    
    def _read_sensor(self) -> float:
        """
        Read distance from the actual sonar sensor (placeholder).
        
        Returns:
            Distance in meters
        """
        # Placeholder implementation
        return 1.5  # Default 1.5 meters
    
    def is_obstacle_detected(self, threshold: float = 0.5) -> bool:
        """
        Check if an obstacle is detected within the threshold distance.
        
        Args:
            threshold: Distance threshold in meters (default: 0.5m)
            
        Returns:
            True if obstacle detected within threshold, False otherwise
        """
        if not self._enabled:
            return False
        
        reading = self.get_distance()
        return reading.distance < threshold
    
    @property
    def enabled(self) -> bool:
        """Check if sonar sensor is enabled."""
        return self._enabled
