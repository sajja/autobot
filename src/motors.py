"""Motor control classes for the autonomous vehicle."""

from enum import Enum
from typing import Tuple
import time


class Direction(Enum):
    """Direction of motor rotation."""
    
    CLOCKWISE = 1
    COUNTERCLOCKWISE = -1


class StepperMotor:
    """
    Stepper motor controller for precise movement control.
    """
    
    def __init__(self, motor_id: int, steps_per_revolution: int = 200):
        """
        Initialize a stepper motor.
        
        Args:
            motor_id: Unique identifier for the motor (1-4)
            steps_per_revolution: Number of steps per full revolution (default: 200)
        """
        self.motor_id = motor_id
        self.steps_per_revolution = steps_per_revolution
        self._current_position = 0  # Current position in steps
        self._speed = 100  # Steps per second
        self._enabled = False
        self._direction = Direction.CLOCKWISE
    
    def enable(self) -> None:
        """Enable the motor (energize coils)."""
        self._enabled = True
        print(f"Motor {self.motor_id}: Enabled")
    
    def disable(self) -> None:
        """Disable the motor (de-energize coils)."""
        self._enabled = False
        print(f"Motor {self.motor_id}: Disabled")
    
    def set_speed(self, steps_per_second: int) -> None:
        """
        Set the motor speed.
        
        Args:
            steps_per_second: Speed in steps per second
        """
        if steps_per_second <= 0:
            raise ValueError("Speed must be positive")
        self._speed = steps_per_second
        print(f"Motor {self.motor_id}: Speed set to {steps_per_second} steps/sec")
    
    def set_direction(self, direction: Direction) -> None:
        """
        Set the rotation direction.
        
        Args:
            direction: Direction.CLOCKWISE or Direction.COUNTERCLOCKWISE
        """
        self._direction = direction
        print(f"Motor {self.motor_id}: Direction set to {direction.name}")
    
    def step(self, num_steps: int) -> None:
        """
        Move the motor by a specified number of steps.
        
        Args:
            num_steps: Number of steps to move (positive or negative)
        """
        if not self._enabled:
            raise RuntimeError(f"Motor {self.motor_id} is not enabled")
        
        # Set direction based on sign of num_steps
        if num_steps < 0:
            self.set_direction(Direction.COUNTERCLOCKWISE)
            num_steps = abs(num_steps)
        else:
            self.set_direction(Direction.CLOCKWISE)
        
        # Simulate stepping (in real implementation, this would control actual hardware)
        self._current_position += num_steps * self._direction.value
        print(f"Motor {self.motor_id}: Stepped {num_steps} steps, position: {self._current_position}")
    
    def rotate_degrees(self, degrees: float) -> None:
        """
        Rotate the motor by a specified number of degrees.
        
        Args:
            degrees: Degrees to rotate (positive or negative)
        """
        steps = int((degrees / 360.0) * self.steps_per_revolution)
        self.step(steps)
    
    def stop(self) -> None:
        """Stop the motor immediately."""
        print(f"Motor {self.motor_id}: Stopped")
    
    def reset_position(self) -> None:
        """Reset the position counter to zero."""
        self._current_position = 0
        print(f"Motor {self.motor_id}: Position reset")
    
    @property
    def position(self) -> int:
        """Get the current position in steps."""
        return self._current_position
    
    @property
    def enabled(self) -> bool:
        """Check if motor is enabled."""
        return self._enabled


class MotorController:
    """
    Controller for managing 4 stepper motors for vehicle mobility.
    Typically configured as: Front-Left, Front-Right, Rear-Left, Rear-Right
    """
    
    def __init__(self):
        """Initialize the motor controller with 4 stepper motors."""
        self.front_left = StepperMotor(motor_id=1)
        self.front_right = StepperMotor(motor_id=2)
        self.rear_left = StepperMotor(motor_id=3)
        self.rear_right = StepperMotor(motor_id=4)
        self.motors = [self.front_left, self.front_right, self.rear_left, self.rear_right]
    
    def enable_all(self) -> None:
        """Enable all motors."""
        for motor in self.motors:
            motor.enable()
    
    def disable_all(self) -> None:
        """Disable all motors."""
        for motor in self.motors:
            motor.disable()
    
    def stop_all(self) -> None:
        """Stop all motors immediately."""
        for motor in self.motors:
            motor.stop()
    
    def set_all_speeds(self, speed: int) -> None:
        """
        Set the same speed for all motors.
        
        Args:
            speed: Speed in steps per second
        """
        for motor in self.motors:
            motor.set_speed(speed)
    
    def move_forward(self, steps: int) -> None:
        """
        Move the vehicle forward.
        
        Args:
            steps: Number of steps to move forward
        """
        print(f"Moving forward {steps} steps")
        for motor in self.motors:
            motor.step(steps)
    
    def move_backward(self, steps: int) -> None:
        """
        Move the vehicle backward.
        
        Args:
            steps: Number of steps to move backward
        """
        print(f"Moving backward {steps} steps")
        for motor in self.motors:
            motor.step(-steps)
    
    def turn_left(self, steps: int) -> None:
        """
        Turn the vehicle left (left wheels backward, right wheels forward).
        
        Args:
            steps: Number of steps for the turn
        """
        print(f"Turning left {steps} steps")
        self.front_left.step(-steps)
        self.rear_left.step(-steps)
        self.front_right.step(steps)
        self.rear_right.step(steps)
    
    def turn_right(self, steps: int) -> None:
        """
        Turn the vehicle right (right wheels backward, left wheels forward).
        
        Args:
            steps: Number of steps for the turn
        """
        print(f"Turning right {steps} steps")
        self.front_left.step(steps)
        self.rear_left.step(steps)
        self.front_right.step(-steps)
        self.rear_right.step(-steps)
    
    def rotate_in_place(self, steps: int, clockwise: bool = True) -> None:
        """
        Rotate the vehicle in place.
        
        Args:
            steps: Number of steps to rotate
            clockwise: If True, rotate clockwise; if False, rotate counterclockwise
        """
        direction = "clockwise" if clockwise else "counterclockwise"
        print(f"Rotating {direction} {steps} steps")
        
        multiplier = 1 if clockwise else -1
        self.front_left.step(multiplier * steps)
        self.rear_left.step(multiplier * steps)
        self.front_right.step(-multiplier * steps)
        self.rear_right.step(-multiplier * steps)
