"""Visualize LIDAR coverage area in the environment."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.environment import Environment
from src.bot import Bot
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


def visualize_lidar_coverage():
    """Show LIDAR coverage area vs environment size."""
    
    # Create environment
    env = Environment(width=25.0, height=25.0, resolution=0.1)
    
    # Place bot at center
    bot_x, bot_y = 12.5, 12.5
    env.set_bot_position(bot_x, bot_y, orientation=0.0)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Draw environment boundary
    ax.set_xlim(0, 25)
    ax.set_ylim(0, 25)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('X (meters)', fontsize=12)
    ax.set_ylabel('Y (meters)', fontsize=12)
    ax.set_title('LIDAR Coverage Area (10m range) in 25m × 25m Environment', 
                 fontsize=14, fontweight='bold')
    
    # Draw environment boundary
    boundary = patches.Rectangle((0, 0), 25, 25, 
                                 fill=False, edgecolor='black', linewidth=3)
    ax.add_patch(boundary)
    
    # Draw LIDAR coverage circle (10m diameter = 10m max range)
    lidar_range = 10.0
    coverage = patches.Circle((bot_x, bot_y), lidar_range, 
                             fill=True, facecolor='lightblue', 
                             edgecolor='blue', linewidth=2, alpha=0.3,
                             label=f'LIDAR Coverage ({lidar_range}m range)')
    ax.add_patch(coverage)
    
    # Draw bot
    bot_circle = patches.Circle((bot_x, bot_y), 0.5, 
                               color='red', label='Bot')
    ax.add_patch(bot_circle)
    
    # Draw range lines at different distances
    angles = np.linspace(0, 360, 8, endpoint=False)
    for angle in angles:
        rad = np.radians(angle)
        end_x = bot_x + lidar_range * np.cos(rad)
        end_y = bot_y + lidar_range * np.sin(rad)
        ax.plot([bot_x, end_x], [bot_y, end_y], 'b--', alpha=0.5, linewidth=1)
    
    # Mark corners (unreachable from center)
    corners = [(0, 0), (25, 0), (0, 25), (25, 25)]
    for cx, cy in corners:
        distance = np.sqrt((cx - bot_x)**2 + (cy - bot_y)**2)
        color = 'green' if distance <= lidar_range else 'red'
        marker = 'o' if distance <= lidar_range else 'x'
        ax.plot(cx, cy, marker, color=color, markersize=12, 
               markeredgewidth=2)
        ax.text(cx, cy-1, f'{distance:.1f}m', ha='center', fontsize=9)
    
    # Add annotations
    ax.text(12.5, 23, 'Environment: 25m × 25m', 
           ha='center', fontsize=11, fontweight='bold',
           bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    
    ax.text(12.5, 1, f'LIDAR: {lidar_range}m max range\nCoverage: {(lidar_range*2)**2:.0f}m² of {25**2}m²', 
           ha='center', fontsize=10,
           bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
    
    # Add legend
    ax.legend(loc='upper right', fontsize=10)
    
    # Add grid reference
    ax.text(0.5, 24, '✓ = Reachable\n✗ = Out of range', 
           fontsize=9, verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('lidar_coverage.png', dpi=150)
    print("LIDAR coverage visualization saved to 'lidar_coverage.png'")
    plt.show()


if __name__ == "__main__":
    print("Visualizing LIDAR coverage area...")
    print("LIDAR Range: 10m")
    print("Environment: 25m × 25m")
    print()
    visualize_lidar_coverage()
