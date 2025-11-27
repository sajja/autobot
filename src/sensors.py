"""Sensor classes for the autonomous vehicle."""

from typing import List, Tuple
import time
from dataclasses import dataclass


@dataclass
class LidarReading:
    """Represents a single LIDAR reading."""
    
    angle: float  # Angle in degrees (0-360)
    distance: float  # Distance in meters
    timestamp: float  # Timestamp of the reading


class RotatingLidar:
    """
    Rotating LIDAR sensor for 360-degree mapping.
    Scans at 10Hz (10 times per second).
    """
    
    def __init__(self, scan_frequency: float = 10.0, resolution: int = 360):
        """
        Initialize the LIDAR sensor.
        
        Args:
            scan_frequency: Scanning frequency in Hz (default: 10Hz)
            resolution: Number of points per 360-degree scan (default: 360)
        """
        self.scan_frequency = scan_frequency
        self.resolution = resolution
        self.scan_period = 1.0 / scan_frequency
        self._is_scanning = False
        self._current_angle = 0.0
    
    def start_scanning(self) -> None:
        """Start the LIDAR scanning process."""
        self._is_scanning = True
        print(f"LIDAR: Started scanning at {self.scan_frequency}Hz")
    
    def stop_scanning(self) -> None:
        """Stop the LIDAR scanning process."""
        self._is_scanning = False
        print("LIDAR: Stopped scanning")
    
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
            distance = self._simulate_reading(angle)
            scan_data.append(LidarReading(angle, distance, current_time))
        
        return scan_data
    
    def _simulate_reading(self, angle: float) -> float:
        """
        Simulate a LIDAR reading (placeholder for actual sensor reading).
        
        Args:
            angle: Angle in degrees
            
        Returns:
            Simulated distance in meters
        """
        # Placeholder implementation
        return 5.0  # Default 5 meters
    
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
