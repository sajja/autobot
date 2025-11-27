"""Bot class - Autonomous vehicle with sensors and motors."""

from typing import List, Optional
import time
from .sensors import RotatingLidar, SonarSensor, LidarReading, SonarReading
from .motors import MotorController


class Bot:
    """
    Autonomous vehicle class with sensors and motor control.
    
    Features:
    - Rotating LIDAR sensor (10Hz, 360-degree scanning) for mapping
    - Sonar sensor for immediate obstacle detection
    - 4 stepper motors for mobility
    """
    
    def __init__(self):
        """Initialize the autonomous vehicle bot."""
        # Initialize sensors
        self.lidar = RotatingLidar(scan_frequency=10.0, resolution=360)
        self.sonar = SonarSensor(max_range=4.0, min_range=0.02)
        
        # Initialize motor controller
        self.motors = MotorController()
        
        # State variables
        self._initialized = False
        self._running = False
        
        print("Bot: Initialized")
    
    def initialize(self) -> None:
        """Initialize all systems (sensors and motors)."""
        print("Bot: Initializing systems...")
        
        # Enable sensors
        self.lidar.start_scanning()
        self.sonar.enable()
        
        # Enable motors
        self.motors.enable_all()
        self.motors.set_all_speeds(100)  # Set default speed
        
        self._initialized = True
        print("Bot: All systems initialized and ready")
    
    def shutdown(self) -> None:
        """Shutdown all systems safely."""
        print("Bot: Shutting down...")
        
        # Stop motors
        self.motors.stop_all()
        self.motors.disable_all()
        
        # Disable sensors
        self.lidar.stop_scanning()
        self.sonar.disable()
        
        self._initialized = False
        self._running = False
        print("Bot: Shutdown complete")
    
    def get_lidar_scan(self) -> List[LidarReading]:
        """
        Get a complete 360-degree LIDAR scan.
        
        Returns:
            List of LidarReading objects
        """
        if not self._initialized:
            raise RuntimeError("Bot not initialized. Call initialize() first.")
        
        return self.lidar.get_scan()
    
    def check_obstacles(self, threshold: float = 0.5) -> bool:
        """
        Check for immediate obstacles using sonar sensor.
        
        Args:
            threshold: Distance threshold in meters (default: 0.5m)
            
        Returns:
            True if obstacle detected within threshold, False otherwise
        """
        if not self._initialized:
            raise RuntimeError("Bot not initialized. Call initialize() first.")
        
        return self.sonar.is_obstacle_detected(threshold)
    
    def get_sonar_distance(self) -> SonarReading:
        """
        Get current distance reading from sonar sensor.
        
        Returns:
            SonarReading object with distance and timestamp
        """
        if not self._initialized:
            raise RuntimeError("Bot not initialized. Call initialize() first.")
        
        return self.sonar.get_distance()
    
    # Movement methods
    
    def move_forward(self, steps: int) -> None:
        """
        Move the bot forward.
        
        Args:
            steps: Number of steps to move
        """
        if not self._initialized:
            raise RuntimeError("Bot not initialized. Call initialize() first.")
        
        self.motors.move_forward(steps)
    
    def move_backward(self, steps: int) -> None:
        """
        Move the bot backward.
        
        Args:
            steps: Number of steps to move
        """
        if not self._initialized:
            raise RuntimeError("Bot not initialized. Call initialize() first.")
        
        self.motors.move_backward(steps)
    
    def turn_left(self, steps: int) -> None:
        """
        Turn the bot left.
        
        Args:
            steps: Number of steps for the turn
        """
        if not self._initialized:
            raise RuntimeError("Bot not initialized. Call initialize() first.")
        
        self.motors.turn_left(steps)
    
    def turn_right(self, steps: int) -> None:
        """
        Turn the bot right.
        
        Args:
            steps: Number of steps for the turn
        """
        if not self._initialized:
            raise RuntimeError("Bot not initialized. Call initialize() first.")
        
        self.motors.turn_right(steps)
    
    def rotate(self, steps: int, clockwise: bool = True) -> None:
        """
        Rotate the bot in place.
        
        Args:
            steps: Number of steps to rotate
            clockwise: Rotation direction (default: True)
        """
        if not self._initialized:
            raise RuntimeError("Bot not initialized. Call initialize() first.")
        
        self.motors.rotate_in_place(steps, clockwise)
    
    def stop(self) -> None:
        """Stop all motors immediately."""
        self.motors.stop_all()
    
    def safe_move_forward(self, steps: int, obstacle_threshold: float = 0.5) -> bool:
        """
        Move forward while checking for obstacles with sonar.
        
        Args:
            steps: Number of steps to move
            obstacle_threshold: Distance threshold for obstacle detection (meters)
            
        Returns:
            True if move completed successfully, False if obstacle detected
        """
        if not self._initialized:
            raise RuntimeError("Bot not initialized. Call initialize() first.")
        
        # Check for obstacles before moving
        if self.check_obstacles(obstacle_threshold):
            print("Bot: Obstacle detected! Movement cancelled.")
            return False
        
        self.move_forward(steps)
        return True
    
    def scan_environment(self) -> dict:
        """
        Perform a complete environment scan using all sensors.
        
        Returns:
            Dictionary containing sensor readings
        """
        if not self._initialized:
            raise RuntimeError("Bot not initialized. Call initialize() first.")
        
        lidar_scan = self.get_lidar_scan()
        sonar_reading = self.get_sonar_distance()
        
        return {
            "lidar": {
                "num_points": len(lidar_scan),
                "scan_data": lidar_scan,
                "timestamp": lidar_scan[0].timestamp if lidar_scan else None
            },
            "sonar": {
                "distance": sonar_reading.distance,
                "timestamp": sonar_reading.timestamp
            }
        }
    
    @property
    def is_initialized(self) -> bool:
        """Check if bot is initialized."""
        return self._initialized
    
    @property
    def is_running(self) -> bool:
        """Check if bot is running."""
        return self._running
    
    def __repr__(self) -> str:
        """String representation of the bot."""
        return f"Bot(initialized={self._initialized}, running={self._running})"
