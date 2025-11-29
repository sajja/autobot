"""Environment class for the autonomous vehicle simulation."""

from typing import Tuple, List, Optional, Set, Callable
from dataclasses import dataclass
import time
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
    Default size is 25m x 25m (larger than LIDAR's 10m range).
    """
    
    def __init__(self, width: float = 25.0, height: float = 25.0, resolution: float = 0.1):
        """
        Initialize the environment.
        
        Args:
            width: Width of the environment in meters (default: 25.0m)
            height: Height of the environment in meters (default: 25.0m)
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
            
            # Draw LIDAR range circle (5m range)
            lidar_range = 5.0  # LIDAR max range
            range_circle = Circle((bot_x, bot_y), lidar_range,
                                 fill=False, edgecolor='cyan', linewidth=2,
                                 linestyle='--', alpha=0.6, label='LIDAR Range (5m)')
            ax.add_patch(range_circle)
            
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
        
        # Draw obstacles - keep track of patches for color updates
        obstacle_circles = []
        obstacle_centers = []
        for obstacle in self.obstacles:
            circle = Circle((obstacle.position.x, obstacle.position.y), 
                           obstacle.radius, 
                           color='black', alpha=0.6)  # Start black (not detected)
            ax.add_patch(circle)
            center_point = ax.plot(obstacle.position.x, obstacle.position.y, 'kx', markersize=8)[0]
            obstacle_circles.append(circle)
            obstacle_centers.append(center_point)
        
        # Draw bot if positioned (initially RED - stopped)
        bot_circle = None
        bot_arrow = None
        bot_text = None
        lidar_circle = None
        
        if self.bot_position:
            bot_x = self.bot_position.x
            bot_y = self.bot_position.y
            bot_size = 0.3
            
            # LIDAR range circle (5m range) - initially None (not visible when stopped)
            lidar_range = 5.0
            lidar_circle = None
            
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
        ax_button = plt.axes([0.35, 0.02, 0.15, 0.05])
        btn_control = Button(ax_button, 'Start Bot', color='lightcoral', hovercolor='red')
        
        # Add Place Object button (BLUE)
        ax_obj_button = plt.axes([0.52, 0.02, 0.15, 0.05])
        btn_place_obj = Button(ax_obj_button, 'Place Object', color='lightblue', hovercolor='blue')
        
        # Add Move Bot button (GREEN)
        ax_move_button = plt.axes([0.18, 0.02, 0.15, 0.05])
        btn_move_bot = Button(ax_move_button, 'Move Bot', color='lightgreen', hovercolor='green')
        
        # Track placed obstacles (circles and center points)
        obstacle_patches = []
        obstacle_patch_centers = []
        
        # Track LIDAR wall detection points
        wall_detection_markers = []
        
        # Track placement mode
        placement_mode = [False]  # Use list to allow modification in nested function
        move_bot_mode = [False]  # Track if in bot movement mode
        
        # Move Bot button handler
        def on_move_bot_clicked(event):
            """Toggle move bot mode - click on plot to move bot."""
            if bot_running:
                print("\n⚠️  Cannot move bot while running! Stop the bot first.")
                return
            
            move_bot_mode[0] = not move_bot_mode[0]
            
            if move_bot_mode[0]:
                # Deactivate placement mode if active
                if placement_mode[0]:
                    placement_mode[0] = False
                    btn_place_obj.color = 'lightblue'
                    btn_place_obj.hovercolor = 'blue'
                    btn_place_obj.label.set_text('Place Object')
                
                btn_move_bot.color = 'yellow'
                btn_move_bot.hovercolor = 'orange'
                btn_move_bot.label.set_text('Click to Move')
                print("\n🤖 MOVE BOT MODE: Click on the plot to move the bot")
            else:
                btn_move_bot.color = 'lightgreen'
                btn_move_bot.hovercolor = 'green'
                btn_move_bot.label.set_text('Move Bot')
                print("\n❌ Move bot mode deactivated")
            
            plt.draw()
        
        # Place Object button handler
        def on_place_object_clicked(event):
            """Toggle placement mode - click on plot to place obstacle."""
            # Deactivate move bot mode if active
            if move_bot_mode[0]:
                move_bot_mode[0] = False
                btn_move_bot.color = 'lightgreen'
                btn_move_bot.hovercolor = 'green'
                btn_move_bot.label.set_text('Move Bot')
            
            placement_mode[0] = not placement_mode[0]
            
            if placement_mode[0]:
                btn_place_obj.color = 'yellow'
                btn_place_obj.hovercolor = 'orange'
                btn_place_obj.label.set_text('Click to Place')
                print("\n🖱️  PLACEMENT MODE: Click on the plot to place a 30cm obstacle")
            else:
                btn_place_obj.color = 'lightblue'
                btn_place_obj.hovercolor = 'blue'
                btn_place_obj.label.set_text('Place Object')
                print("\n❌ Placement mode deactivated")
            
            plt.draw()
        
        # Mouse click handler for placing obstacles and moving bot
        def on_plot_click(event):
            """Handle mouse clicks on the plot to place obstacles or move bot."""
            nonlocal bot_circle, bot_arrow, bot_text, lidar_circle
            
            # Check if click is inside the main axes
            if event.inaxes != ax:
                return
            
            x, y = event.xdata, event.ydata
            
            # Handle bot movement
            if move_bot_mode[0]:
                # Check if within bounds
                if not self.is_valid_position(x, y):
                    print(f"\n❌ Position ({x:.2f}, {y:.2f}) is out of bounds")
                    return
                
                # Check if position overlaps with obstacles
                min_distance = 0.5  # Keep 0.5m from obstacles
                for obstacle in self.obstacles:
                    dist = np.sqrt((x - obstacle.position.x)**2 + (y - obstacle.position.y)**2)
                    if dist < obstacle.radius + min_distance:
                        print(f"\n❌ Too close to obstacle! Distance: {dist:.2f}m (min: {min_distance}m)")
                        return
                
                # Move the bot
                old_x = self.bot_position.x if self.bot_position else 0
                old_y = self.bot_position.y if self.bot_position else 0
                
                success = self.set_bot_position(x, y, orientation=self.bot_orientation)
                
                if success:
                    # Update bot visualization
                    if bot_circle:
                        bot_circle.remove()
                    if bot_arrow:
                        bot_arrow.remove()
                    if bot_text:
                        bot_text.remove()
                    
                    bot_size = 0.3
                    # Bot is RED when stopped
                    bot_circle = Circle((x, y), bot_size, 
                                       color='red', alpha=0.7, label='Bot (Stopped)')
                    ax.add_patch(bot_circle)
                    
                    arrow_length = bot_size * 1.5
                    dx = arrow_length * np.cos(np.radians(self.bot_orientation))
                    dy = arrow_length * np.sin(np.radians(self.bot_orientation))
                    bot_arrow = ax.arrow(x, y, dx, dy, 
                                        head_width=0.15, head_length=0.1, 
                                        fc='darkred', ec='darkred', linewidth=2)
                    
                    bot_text = ax.text(x, y - bot_size - 0.3, 
                                      f'Bot (STOPPED)\n({x:.1f}, {y:.1f})\n{self.bot_orientation:.0f}°',
                                      ha='center', va='top', fontsize=9, 
                                      bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.7))
                    
                    # Update LIDAR circle position if it exists
                    if lidar_circle:
                        lidar_circle.set_center((x, y))
                    
                    # Update bot instance position if it exists
                    if bot_instance:
                        bot_instance.position = (x, y)
                        bot_instance.lidar.position = (x, y)
                    
                    plt.draw()
                    print(f"\n✅ Bot moved from ({old_x:.2f}, {old_y:.2f}) to ({x:.2f}, {y:.2f})")
                    
                    # Auto-deactivate move mode after moving
                    move_bot_mode[0] = False
                    btn_move_bot.color = 'lightgreen'
                    btn_move_bot.hovercolor = 'green'
                    btn_move_bot.label.set_text('Move Bot')
                    plt.draw()
                else:
                    print(f"\n❌ Could not move bot to ({x:.2f}, {y:.2f})")
                
                return
            
            # Handle obstacle placement
            if not placement_mode[0]:
                return  # Not in placement mode
            
            obj_size = 0.15  # 15cm radius (30cm diameter)
            
            # Check if within bounds
            if not self.is_valid_position(x, y):
                print(f"\n❌ Position ({x:.2f}, {y:.2f}) is out of bounds")
                return
            
            # Check if too close to bot
            if self.bot_position:
                dist_to_bot = np.sqrt((x - self.bot_position.x)**2 + (y - self.bot_position.y)**2)
                if dist_to_bot < 0.5:  # Keep 0.5m away from bot
                    print(f"\n❌ Too close to bot! Distance: {dist_to_bot:.2f}m (min: 0.5m)")
                    return
            
            # Place the obstacle
            success = self.add_obstacle(x, y, radius=obj_size)
            
            if success:
                # Draw the obstacle on the plot (black initially - not detected)
                obstacle_circle = Circle((x, y), obj_size, 
                                       color='black', alpha=0.6, label='Obstacle')
                ax.add_patch(obstacle_circle)
                obstacle_patches.append(obstacle_circle)
                obstacle_circles.append(obstacle_circle)
                
                # Add center point
                center_pt = ax.plot(x, y, 'kx', markersize=8)[0]
                obstacle_patch_centers.append(center_pt)
                obstacle_centers.append(center_pt)
                
                # Update info box
                info_text_updated = f"Grid: {self.grid_width}×{self.grid_height}\n"
                info_text_updated += f"Resolution: {self.resolution}m\n"
                info_text_updated += f"Obstacles: {len(self.obstacles)}\n"
                if bot_running:
                    info_text_updated += f"Status: Running\nLIDAR: Scanning at {bot_instance.lidar.scan_frequency}Hz"
                else:
                    info_text_updated += f"Status: Stopped"
                info_box.set_text(info_text_updated)
                
                plt.draw()
                print(f"\n✅ Obstacle placed at ({x:.2f}, {y:.2f}) - Size: 30cm diameter")
                
                # Auto-deactivate placement mode after placing
                placement_mode[0] = False
                btn_place_obj.color = 'lightblue'
                btn_place_obj.hovercolor = 'blue'
                btn_place_obj.label.set_text('Place Object')
                plt.draw()
            else:
                print(f"\n❌ Could not place obstacle at ({x:.2f}, {y:.2f})")
        
        # Connect event handlers
        btn_place_obj.on_clicked(on_place_object_clicked)
        btn_move_bot.on_clicked(on_move_bot_clicked)
        fig.canvas.mpl_connect('button_press_event', on_plot_click)
        
        # Button click handler
        def on_button_clicked(event):
            nonlocal bot_running, bot_circle, bot_arrow, bot_text, lidar_circle
            
            if not bot_running:
                # START BOT
                print("\n" + "="*60)
                print("START BOT BUTTON CLICKED!")
                print("="*60)
                
                if bot_instance:
                    # Update bot's environment context
                    if self.bot_position:
                        bot_instance.position = (self.bot_position.x, self.bot_position.y)
                        bot_instance.environment_bounds = (self.width, self.height)
                        # Pass obstacles to LIDAR sensor
                        bot_instance.lidar.position = bot_instance.position
                        bot_instance.lidar.environment_bounds = bot_instance.environment_bounds
                        bot_instance.lidar.obstacles = self.obstacles
                    
                    # Initialize bot
                    if not bot_instance.is_initialized:
                        bot_instance.initialize()
                    
                    # Define callback for continuous LIDAR scans
                    def lidar_scan_callback(scan_data):
                        """Called on each LIDAR scan."""
                        print(f"\n[LIDAR Scan #{bot_instance.lidar._scan_count}] {len(scan_data)} points at {time.time():.2f}")
                        
                        # Update obstacle colors based on LIDAR detection
                        update_obstacle_visibility(scan_data)
                        
                        # Show sample of scan data (first 5 readings)
                        if bot_instance.lidar._scan_count == 1:
                            print("-" * 60)
                            print(f"{'Angle (°)':>12} {'Distance (m)':>15} {'Intensity':>15}")
                            print("-" * 60)
                            for i in range(min(5, len(scan_data))):
                                reading = scan_data[i]
                                print(f"{reading.angle:>12.0f} {reading.distance:>15.2f} {reading.intensity:>15}")
                            print("..." + " " * 53 + "...")
                            print(f"Continuous scanning at {bot_instance.lidar.scan_frequency}Hz...")
                    
                    # Function to update obstacle visibility based on LIDAR detections
                    def update_obstacle_visibility(scan_data):
                        """Update obstacle colors: red if detected by LIDAR, black if not."""
                        nonlocal wall_detection_markers
                        
                        if not scan_data or not self.bot_position:
                            return
                        
                        # Clear previous wall detection markers
                        for marker in wall_detection_markers:
                            marker.remove()
                        wall_detection_markers.clear()
                        
                        # Get detected positions from LIDAR scan
                        detected_positions = []
                        wall_detections = []
                        bot_x = self.bot_position.x
                        bot_y = self.bot_position.y
                        
                        for reading in scan_data:
                            if reading.distance > 0 and reading.distance < bot_instance.lidar.max_range:
                                # Calculate the position of the detected point
                                angle_rad = np.radians(reading.angle)
                                detected_x = bot_x + reading.distance * np.cos(angle_rad)
                                detected_y = bot_y + reading.distance * np.sin(angle_rad)
                                
                                # Check if this is a wall detection (near boundaries)
                                is_wall = False
                                tolerance = 0.2  # 20cm tolerance for wall detection
                                
                                if abs(detected_x - 0) < tolerance:  # Left wall
                                    is_wall = True
                                elif abs(detected_x - self.width) < tolerance:  # Right wall
                                    is_wall = True
                                elif abs(detected_y - 0) < tolerance:  # Bottom wall
                                    is_wall = True
                                elif abs(detected_y - self.height) < tolerance:  # Top wall
                                    is_wall = True
                                
                                if is_wall:
                                    wall_detections.append((detected_x, detected_y))
                                
                                detected_positions.append((detected_x, detected_y))
                        
                        # Plot wall detections as RED dots (highly visible)
                        if wall_detections:
                            wall_x = [pos[0] for pos in wall_detections]
                            wall_y = [pos[1] for pos in wall_detections]
                            # RED dots, larger size for better visibility
                            marker = ax.plot(wall_x, wall_y, 'ro', markersize=6, alpha=0.8, label='Wall Detection')[0]
                            wall_detection_markers.append(marker)
                            
                            # Debug: Print wall detection count
                            if bot_instance.lidar._scan_count == 1:
                                print(f"� Wall detections: {len(wall_detections)} points plotted as RED dots")
                        
                        # Check each obstacle to see if it's detected
                        for i, obstacle in enumerate(self.obstacles):
                            obs_x = obstacle.position.x
                            obs_y = obstacle.position.y
                            obs_radius = obstacle.radius
                            
                            # Check if any detected point is within the obstacle's radius
                            is_detected = False
                            for det_x, det_y in detected_positions:
                                dist = np.sqrt((det_x - obs_x)**2 + (det_y - obs_y)**2)
                                if dist <= obs_radius + 0.1:  # Small tolerance
                                    is_detected = True
                                    break
                            
                            # Update obstacle color
                            if i < len(obstacle_circles):
                                if is_detected:
                                    obstacle_circles[i].set_color('red')
                                    obstacle_circles[i].set_alpha(0.7)
                                    if i < len(obstacle_centers):
                                        obstacle_centers[i].set_color('red')
                                else:
                                    obstacle_circles[i].set_color('black')
                                    obstacle_circles[i].set_alpha(0.6)
                                    if i < len(obstacle_centers):
                                        obstacle_centers[i].set_color('black')
                        
                        # Redraw the plot
                        plt.draw()
                    
                    # Start bot with continuous LIDAR scanning
                    print("\n--- Starting Continuous LIDAR Scanning ---")
                    bot_instance.start(lidar_callback=lidar_scan_callback)
                    
                    # Get initial scan for display
                    time.sleep(0.5)  # Wait for first scan
                    scan_data = bot_instance.get_latest_lidar_scan()
                    
                    if scan_data:
                        print(f"\nInitial scan: {len(scan_data)} readings")
                    else:
                        scan_data = []
                        print("\nWaiting for first scan...")
                    
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
                    
                    # Show LIDAR circle in CYAN (active scanning)
                    if lidar_circle is None:
                        # Create new LIDAR circle
                        lidar_circle = Circle((bot_x, bot_y), lidar_range,
                                            fill=False, edgecolor='cyan', linewidth=2,
                                            linestyle='--', alpha=0.6, label='LIDAR Range (5m)')
                        ax.add_patch(lidar_circle)
                    else:
                        # Just update existing circle
                        lidar_circle.set_visible(True)
                        lidar_circle.set_edgecolor('cyan')
                        lidar_circle.set_alpha(0.6)
                    
                    # Update status
                    info_text_updated = f"Grid: {self.grid_width}×{self.grid_height}\n"
                    info_text_updated += f"Resolution: {self.resolution}m\n"
                    info_text_updated += f"Obstacles: {len(self.obstacles)}\n"
                    info_text_updated += f"Status: Running\nLIDAR: Scanning at {bot_instance.lidar.scan_frequency}Hz"
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
                    
                    # Clear wall detection markers
                    for marker in wall_detection_markers:
                        marker.remove()
                    wall_detection_markers.clear()
                    
                    # Reset all obstacles to black (not detected)
                    for i, obstacle in enumerate(self.obstacles):
                        if i < len(obstacle_circles):
                            obstacle_circles[i].set_color('black')
                            obstacle_circles[i].set_alpha(0.6)
                            if i < len(obstacle_centers):
                                obstacle_centers[i].set_color('black')
                    
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
                    
                    # Hide LIDAR circle (inactive - not scanning)
                    if lidar_circle:
                        lidar_circle.set_visible(False)
                    
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
