"""Environment class for the autonomous vehicle simulation."""

from typing import Tuple, List, Optional, Set, Callable
from dataclasses import dataclass
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Circle, Wedge, Rectangle
from matplotlib.widgets import Button


@dataclass
class Position:
    """Represents a 2D position in the environment."""
    
    x: float
    y: float
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __eq__(self, other):
        if not isinstance(other, Position):
            return False
        return self.x == other.x and self.y == other.y
    
    def distance_to(self, other: 'Position') -> float:
        """Calculate Euclidean distance to another position."""
        return np.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)


@dataclass
class Obstacle:
    """Represents an obstacle in the environment."""
    
    position: Position
    radius: float  # Circular obstacles for simplicity
    
    def contains_point(self, point: Position) -> bool:
        """Check if a point is inside this obstacle."""
        return point.distance_to(self.position) <= self.radius


class Environment:
    """
    Represents the environment where the bot operates.
    Uses a grid-based coordinate system with continuous positions.
    """
    
    def __init__(self, width: float = 10.0, height: float = 10.0, resolution: float = 0.1):
        """
        Initialize the environment.
        
        Args:
            width: Width of the environment in meters (default: 10.0m)
            height: Height of the environment in meters (default: 10.0m)
            resolution: Grid resolution in meters (default: 0.1m)
        """
        self.width = width
        self.height = height
        self.resolution = resolution
        
        # Calculate grid dimensions
        self.grid_width = int(width / resolution)
        self.grid_height = int(height / resolution)
        
        # Initialize empty grid (0 = free space, 1 = obstacle)
        self.grid = np.zeros((self.grid_height, self.grid_width), dtype=int)
        
        # Store obstacles as objects
        self.obstacles: List[Obstacle] = []
        
        # Bot position and orientation
        self.bot_position: Optional[Position] = None
        self.bot_orientation: float = 0.0  # Angle in degrees (0 = facing right/east)
        
        print(f"Environment: Created {width}m x {height}m environment")
        print(f"Environment: Grid size {self.grid_width} x {self.grid_height} (resolution: {resolution}m)")
    
    def set_bot_position(self, x: float, y: float, orientation: float = 0.0) -> bool:
        """
        Place the bot at a specific position in the environment.
        
        Args:
            x: X coordinate in meters
            y: Y coordinate in meters
            orientation: Orientation angle in degrees (default: 0.0)
            
        Returns:
            True if position is valid, False otherwise
        """
        if not self.is_valid_position(x, y):
            print(f"Environment: Invalid position ({x}, {y}) - out of bounds")
            return False
        
        position = Position(x, y)
        
        # Check if position collides with obstacles
        if self.is_position_occupied(position):
            print(f"Environment: Position ({x}, {y}) is occupied by obstacle")
            return False
        
        self.bot_position = position
        self.bot_orientation = orientation % 360
        print(f"Environment: Bot placed at ({x:.2f}, {y:.2f}) facing {self.bot_orientation:.1f}°")
        return True
    
    def add_obstacle(self, x: float, y: float, radius: float = 0.5) -> bool:
        """
        Add a circular obstacle to the environment.
        
        Args:
            x: X coordinate of obstacle center
            y: Y coordinate of obstacle center
            radius: Radius of the obstacle in meters (default: 0.5m)
            
        Returns:
            True if obstacle added successfully, False otherwise
        """
        if not self.is_valid_position(x, y):
            print(f"Environment: Cannot add obstacle at ({x}, {y}) - out of bounds")
            return False
        
        obstacle = Obstacle(Position(x, y), radius)
        self.obstacles.append(obstacle)
        
        # Update grid
        self._update_grid_with_obstacle(obstacle)
        
        print(f"Environment: Added obstacle at ({x:.2f}, {y:.2f}) with radius {radius:.2f}m")
        return True
    
    def _update_grid_with_obstacle(self, obstacle: Obstacle) -> None:
        """Update the grid to mark obstacle cells."""
        # Calculate grid cells affected by this obstacle
        min_x = max(0, int((obstacle.position.x - obstacle.radius) / self.resolution))
        max_x = min(self.grid_width - 1, int((obstacle.position.x + obstacle.radius) / self.resolution))
        min_y = max(0, int((obstacle.position.y - obstacle.radius) / self.resolution))
        max_y = min(self.grid_height - 1, int((obstacle.position.y + obstacle.radius) / self.resolution))
        
        for i in range(min_y, max_y + 1):
            for j in range(min_x, max_x + 1):
                # Convert grid coordinates to world coordinates
                world_x = j * self.resolution + self.resolution / 2
                world_y = i * self.resolution + self.resolution / 2
                point = Position(world_x, world_y)
                
                if obstacle.contains_point(point):
                    self.grid[i, j] = 1
    
    def remove_all_obstacles(self) -> None:
        """Remove all obstacles from the environment."""
        self.obstacles.clear()
        self.grid = np.zeros((self.grid_height, self.grid_width), dtype=int)
        print("Environment: All obstacles removed")
    
    def is_valid_position(self, x: float, y: float) -> bool:
        """
        Check if a position is within the environment bounds.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            True if position is valid, False otherwise
        """
        return 0 <= x <= self.width and 0 <= y <= self.height
    
    def is_position_occupied(self, position: Position) -> bool:
        """
        Check if a position is occupied by an obstacle.
        
        Args:
            position: Position to check
            
        Returns:
            True if position is occupied, False otherwise
        """
        for obstacle in self.obstacles:
            if obstacle.contains_point(position):
                return True
        return False
    
    def get_grid_value(self, x: float, y: float) -> int:
        """
        Get the grid value at a specific world coordinate.
        
        Args:
            x: X coordinate in meters
            y: Y coordinate in meters
            
        Returns:
            Grid value (0 = free, 1 = obstacle, -1 = out of bounds)
        """
        if not self.is_valid_position(x, y):
            return -1
        
        grid_x = int(x / self.resolution)
        grid_y = int(y / self.resolution)
        
        # Clamp to grid bounds
        grid_x = min(grid_x, self.grid_width - 1)
        grid_y = min(grid_y, self.grid_height - 1)
        
        return self.grid[grid_y, grid_x]
    
    def get_occupancy_grid(self) -> np.ndarray:
        """
        Get the occupancy grid representation.
        
        Returns:
            2D numpy array representing the environment (0 = free, 1 = obstacle)
        """
        return self.grid.copy()
    
    def display(self) -> str:
        """
        Create a text representation of the environment.
        
        Returns:
            String representation of the environment
        """
        # Create a simplified view (reduce resolution for display)
        display_resolution = max(1, int(0.5 / self.resolution))  # Show 0.5m cells
        display_height = self.grid_height // display_resolution
        display_width = self.grid_width // display_resolution
        
        lines = []
        lines.append("=" * (display_width + 2))
        
        for i in range(display_height):
            row = "|"
            for j in range(display_width):
                # Sample the grid at this display cell
                grid_i = i * display_resolution
                grid_j = j * display_resolution
                
                # Check if bot is in this cell
                bot_here = False
                if self.bot_position:
                    bot_grid_x = int(self.bot_position.x / self.resolution)
                    bot_grid_y = int(self.bot_position.y / self.resolution)
                    if (grid_j <= bot_grid_x < grid_j + display_resolution and
                        grid_i <= bot_grid_y < grid_i + display_resolution):
                        bot_here = True
                
                if bot_here:
                    row += "B"  # Bot
                elif self.grid[grid_i, grid_j] == 1:
                    row += "#"  # Obstacle
                else:
                    row += " "  # Free space
            
            row += "|"
            lines.append(row)
        
        lines.append("=" * (display_width + 2))
        
        # Add legend and info
        lines.append(f"Size: {self.width}m x {self.height}m")
        lines.append(f"Obstacles: {len(self.obstacles)}")
        if self.bot_position:
            lines.append(f"Bot: ({self.bot_position.x:.2f}, {self.bot_position.y:.2f}) @ {self.bot_orientation:.1f}°")
        else:
            lines.append("Bot: Not placed")
        lines.append("Legend: B=Bot, #=Obstacle, ' '=Free space")
        
        return "\n".join(lines)
    
    def get_info(self) -> dict:
        """
        Get environment information.
        
        Returns:
            Dictionary containing environment details
        """
        return {
            "width": self.width,
            "height": self.height,
            "resolution": self.resolution,
            "grid_size": (self.grid_width, self.grid_height),
            "num_obstacles": len(self.obstacles),
            "bot_position": (self.bot_position.x, self.bot_position.y) if self.bot_position else None,
            "bot_orientation": self.bot_orientation if self.bot_position else None,
            "occupied_cells": int(np.sum(self.grid)),
            "free_cells": int(np.sum(self.grid == 0))
        }
    
    def visualize(self, show: bool = True, save_path: Optional[str] = None, figsize: Tuple[int, int] = (10, 10)) -> None:
        """
        Create a graphical visualization of the environment using matplotlib.
        
        Args:
            show: If True, display the plot (default: True)
            save_path: Optional path to save the figure
            figsize: Figure size in inches (default: (10, 10))
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        # Set up the plot
        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
        ax.set_xlabel('X (meters)', fontsize=12)
        ax.set_ylabel('Y (meters)', fontsize=12)
        ax.set_title(f'Environment: {self.width}m × {self.height}m | Obstacles: {len(self.obstacles)}', 
                     fontsize=14, fontweight='bold')
        
        # Draw boundary
        boundary = Rectangle((0, 0), self.width, self.height, 
                             fill=False, edgecolor='black', linewidth=2)
        ax.add_patch(boundary)
        
        # Draw obstacles
        for obstacle in self.obstacles:
            circle = Circle((obstacle.position.x, obstacle.position.y), 
                           obstacle.radius, 
                           color='red', alpha=0.6, label='Obstacle')
            ax.add_patch(circle)
            # Add obstacle center point
            ax.plot(obstacle.position.x, obstacle.position.y, 'rx', markersize=8)
        
        # Draw bot if positioned
        if self.bot_position:
            bot_x = self.bot_position.x
            bot_y = self.bot_position.y
            bot_size = 0.3  # Bot size in meters
            
            # Draw bot body as a circle
            bot_circle = Circle((bot_x, bot_y), bot_size, 
                               color='blue', alpha=0.7, label='Bot')
            ax.add_patch(bot_circle)
            
            # Draw direction indicator (arrow showing orientation)
            arrow_length = bot_size * 1.5
            dx = arrow_length * np.cos(np.radians(self.bot_orientation))
            dy = arrow_length * np.sin(np.radians(self.bot_orientation))
            ax.arrow(bot_x, bot_y, dx, dy, 
                    head_width=0.15, head_length=0.1, 
                    fc='darkblue', ec='darkblue', linewidth=2)
            
            # Add bot position text
            ax.text(bot_x, bot_y - bot_size - 0.3, 
                   f'Bot\n({bot_x:.1f}, {bot_y:.1f})\n{self.bot_orientation:.0f}°',
                   ha='center', va='top', fontsize=9, 
                   bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
        
        # Add legend (remove duplicates)
        handles, labels = ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        if by_label:
            ax.legend(by_label.values(), by_label.keys(), loc='upper right', fontsize=10)
        
        # Add info box
        info_text = f"Grid: {self.grid_width}×{self.grid_height}\n"
        info_text += f"Resolution: {self.resolution}m\n"
        info_text += f"Free cells: {int(np.sum(self.grid == 0))}\n"
        info_text += f"Occupied: {int(np.sum(self.grid))}"
        
        ax.text(0.02, 0.98, info_text, transform=ax.transAxes,
               fontsize=9, verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        plt.tight_layout()
        
        # Save if path provided
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"Environment: Visualization saved to {save_path}")
        
        # Show if requested
        if show:
            plt.show()
        
        return fig, ax
    
    def visualize_interactive(self, bot_instance=None, on_start_callback: Optional[Callable] = None) -> None:
        """
        Create an interactive visualization with controls.
        Bot colors: Red (stopped), Blue (running)
        Button: Red "Start Bot" -> Green "Stop Bot"
        
        Args:
            bot_instance: Optional Bot instance to control
            on_start_callback: Callback function when Start Bot button is pressed
        """
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # State variable
        bot_running = False
        
        # Set up the plot
        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
        ax.set_xlabel('X (meters)', fontsize=12)
        ax.set_ylabel('Y (meters)', fontsize=12)
        ax.set_title(f'Interactive Environment: {self.width}m × {self.height}m', 
                     fontsize=14, fontweight='bold')
        
        # Draw boundary
        boundary = Rectangle((0, 0), self.width, self.height, 
                             fill=False, edgecolor='black', linewidth=2)
        ax.add_patch(boundary)
        
        # Draw obstacles
        for obstacle in self.obstacles:
            circle = Circle((obstacle.position.x, obstacle.position.y), 
                           obstacle.radius, 
                           color='red', alpha=0.6)
            ax.add_patch(circle)
            ax.plot(obstacle.position.x, obstacle.position.y, 'rx', markersize=8)
        
        # Draw bot if positioned (initially RED - stopped)
        bot_circle = None
        bot_arrow = None
        bot_text = None
        
        if self.bot_position:
            bot_x = self.bot_position.x
            bot_y = self.bot_position.y
            bot_size = 0.3
            
            # Bot starts RED (stopped)
            bot_circle = Circle((bot_x, bot_y), bot_size, 
                               color='red', alpha=0.7, label='Bot (Stopped)')
            ax.add_patch(bot_circle)
            
            arrow_length = bot_size * 1.5
            dx = arrow_length * np.cos(np.radians(self.bot_orientation))
            dy = arrow_length * np.sin(np.radians(self.bot_orientation))
            bot_arrow = ax.arrow(bot_x, bot_y, dx, dy, 
                                head_width=0.15, head_length=0.1, 
                                fc='darkred', ec='darkred', linewidth=2)
            
            bot_text = ax.text(bot_x, bot_y - bot_size - 0.3, 
                              f'Bot (STOPPED)\n({bot_x:.1f}, {bot_y:.1f})\n{self.bot_orientation:.0f}°',
                              ha='center', va='top', fontsize=9, 
                              bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.7))
        
        # Add info text
        info_text = f"Grid: {self.grid_width}×{self.grid_height}\n"
        info_text += f"Resolution: {self.resolution}m\n"
        info_text += f"Obstacles: {len(self.obstacles)}\n"
        info_text += f"Status: Stopped"
        
        info_box = ax.text(0.02, 0.98, info_text, transform=ax.transAxes,
                          fontsize=9, verticalalignment='top',
                          bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        # Add Start Bot button (RED initially)
        ax_button = plt.axes([0.4, 0.02, 0.2, 0.05])
        btn_control = Button(ax_button, 'Start Bot', color='lightcoral', hovercolor='red')
        
        # Button click handler
        def on_button_clicked(event):
            nonlocal bot_running, bot_circle, bot_arrow, bot_text
            
            if not bot_running:
                # START BOT
                print("\n" + "="*60)
                print("START BOT BUTTON CLICKED!")
                print("="*60)
                
                if bot_instance:
                    # Initialize bot
                    if not bot_instance.is_initialized:
                        bot_instance.initialize()
                    
                    # Start LIDAR scan
                    print("\n--- Starting LIDAR Scan ---")
                    scan_data = bot_instance.get_lidar_scan()
                    
                    # Display scan data in table format
                    print(f"\nLIDAR Scan Results (Total: {len(scan_data)} readings)")
                    print(f"Scan Frequency: {bot_instance.lidar.scan_frequency} Hz")
                    print("-" * 60)
                    print(f"{'Angle (°)':>12} {'Distance (m)':>15} {'Intensity':>15}")
                    print("-" * 60)
                    
                    # Show first 10, middle 5, and last 10 readings
                    show_indices = list(range(10)) + list(range(175, 180)) + list(range(350, 360))
                    
                    for i in show_indices:
                        if i < len(scan_data):
                            reading = scan_data[i]
                            print(f"{reading.angle:>12.0f} {reading.distance:>15.2f} {reading.intensity:>15}")
                            if i == 9:
                                print("..." + " " * 53 + "...")
                            elif i == 179:
                                print("..." + " " * 53 + "...")
                    
                    print("-" * 60)
                    print(f"Scan completed at {scan_data[0].timestamp:.2f}")
                    
                    # Update bot to BLUE (running)
                    if bot_circle and self.bot_position:
                        bot_circle.set_color('blue')
                        if bot_arrow:
                            bot_arrow.remove()
                        bot_x = self.bot_position.x
                        bot_y = self.bot_position.y
                        bot_size = 0.3
                        arrow_length = bot_size * 1.5
                        dx = arrow_length * np.cos(np.radians(self.bot_orientation))
                        dy = arrow_length * np.sin(np.radians(self.bot_orientation))
                        bot_arrow = ax.arrow(bot_x, bot_y, dx, dy, 
                                           head_width=0.15, head_length=0.1, 
                                           fc='darkblue', ec='darkblue', linewidth=2)
                        if bot_text:
                            bot_text.set_text(f'Bot (RUNNING)\n({bot_x:.1f}, {bot_y:.1f})\n{self.bot_orientation:.0f}°')
                            bot_text.set_bbox(dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
                    
                    # Update status
                    info_text_updated = f"Grid: {self.grid_width}×{self.grid_height}\n"
                    info_text_updated += f"Resolution: {self.resolution}m\n"
                    info_text_updated += f"Obstacles: {len(self.obstacles)}\n"
                    info_text_updated += f"Status: Running\nLIDAR: Active ({len(scan_data)} pts)"
                    info_box.set_text(info_text_updated)
                    
                    # Change button to GREEN "Stop Bot"
                    btn_control.label.set_text('Stop Bot')
                    btn_control.color = 'lightgreen'
                    btn_control.hovercolor = 'green'
                    
                    bot_running = True
                    plt.draw()
                    
                    # Call custom callback if provided
                    if on_start_callback:
                        on_start_callback(bot_instance, scan_data)
                else:
                    print("No bot instance provided!")
                    info_box.set_text(f"Grid: {self.grid_width}×{self.grid_height}\n"
                                     f"Resolution: {self.resolution}m\n"
                                     f"Obstacles: {len(self.obstacles)}\n"
                                     f"Status: No bot connected!")
                    plt.draw()
            
            else:
                # STOP BOT
                print("\n" + "="*60)
                print("STOP BOT BUTTON CLICKED!")
                print("="*60)
                
                if bot_instance:
                    # Stop the bot
                    bot_instance.stop()
                    print("Bot stopped!")
                    
                    # Update bot to RED (stopped)
                    if bot_circle and self.bot_position:
                        bot_circle.set_color('red')
                        if bot_arrow:
                            bot_arrow.remove()
                        bot_x = self.bot_position.x
                        bot_y = self.bot_position.y
                        bot_size = 0.3
                        arrow_length = bot_size * 1.5
                        dx = arrow_length * np.cos(np.radians(self.bot_orientation))
                        dy = arrow_length * np.sin(np.radians(self.bot_orientation))
                        bot_arrow = ax.arrow(bot_x, bot_y, dx, dy, 
                                           head_width=0.15, head_length=0.1, 
                                           fc='darkred', ec='darkred', linewidth=2)
                        if bot_text:
                            bot_text.set_text(f'Bot (STOPPED)\n({bot_x:.1f}, {bot_y:.1f})\n{self.bot_orientation:.0f}°')
                            bot_text.set_bbox(dict(boxstyle='round', facecolor='lightcoral', alpha=0.7))
                    
                    # Update status
                    info_box.set_text(f"Grid: {self.grid_width}×{self.grid_height}\n"
                                     f"Resolution: {self.resolution}m\n"
                                     f"Obstacles: {len(self.obstacles)}\n"
                                     f"Status: Stopped")
                    
                    # Change button to RED "Start Bot"
                    btn_control.label.set_text('Start Bot')
                    btn_control.color = 'lightcoral'
                    btn_control.hovercolor = 'red'
                    
                    bot_running = False
                    plt.draw()
        
        btn_control.on_clicked(on_button_clicked)
        
        plt.tight_layout()
        plt.show()
    
    def __repr__(self) -> str:
        """String representation of the environment."""
        return f"Environment({self.width}m x {self.height}m, {len(self.obstacles)} obstacles)"
