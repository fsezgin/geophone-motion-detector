import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def create_real_time_plot(A):
    """
    Creates a real-time line plot to visualize per-second average values as they are received.

    Args:
        A (list): List of per-second average values to be plotted in real time.
    """

    def update_graph(frame):
        """
        Updates the graph with new data on each animation frame.

        Args:
            frame (int): The current frame number for the animation (used to control plot updates).
        """
        ax.clear()  # Clears the current plot to avoid overlap of previous data

        # Plot the per-second average (A) values as a line with markers
        ax.plot(A, label="A (Per-Second Average)", color="green", linestyle='-', marker='o')

        # Set the title and axis labels
        ax.set_title("Per-Second Average (A) Over Time")
        ax.set_xlabel("Time (seconds)")
        ax.set_ylabel("Value")
        ax.legend()  # Display the legend for the plot

    # Create the figure and axis for the plot
    fig, ax = plt.subplots(figsize=(10, 6))

    # Initialize the animation to update the plot every second (1000 ms)
    ani = FuncAnimation(fig, update_graph, interval=1000, cache_frame_data=False)

    # Adjust layout to prevent clipping and ensure everything is displayed properly
    plt.tight_layout()

    # Show the plot window
    plt.show()