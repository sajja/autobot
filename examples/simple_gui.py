"""Simple example showing GUI visualization of the environment."""

from src.environment import Environment


def main():
    """Create and visualize a simple environment."""
    
    # Create a 10m x 10m environment
    env = Environment(width=10.0, height=10.0, resolution=0.1)
    
    # Place the bot
    env.set_bot_position(x=5.0, y=5.0, orientation=45.0)
    
    # Visualize the environment (shows GUI window)
    print("Displaying environment visualization...")
    print("Close the window when done viewing.")
    env.visualize(show=True)
    
    # You can also save the visualization
    env.visualize(show=False, save_path="environment.png")
    print("Visualization saved to environment.png")


if __name__ == "__main__":
    main()
