"""Simple example showing GUI visualization of the environment."""

from src.environment import Environment


def main():
    """Create and visualize a simple environment."""
    
    # Create a 25m x 25m environment (larger than LIDAR's 10m range)
    env = Environment(width=25.0, height=25.0, resolution=0.1)
    
    # Place the bot in center
    env.set_bot_position(x=12.5, y=12.5, orientation=45.0)
    
    # Visualize the environment (shows GUI window)
    print("Displaying environment visualization...")
    print("Environment: 25m x 25m (LIDAR range: 10m)")
    print("Close the window when done viewing.")
    env.visualize(show=True)
    
    # You can also save the visualization
    env.visualize(show=False, save_path="environment.png")
    print("Visualization saved to environment.png")


if __name__ == "__main__":
    main()
