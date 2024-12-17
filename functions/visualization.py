import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def create_real_time_plot(means, top_3_means):
    """
    Creates a real-time graph for visualizing data.

    Args:
        means (list): List of mean values.
        top_3_means (list): List of top 3 mean values.
    """

    def update_graph(frame):
        ax.clear()

        # Mean line
        ax.plot(means, label="Mean", color="blue", linestyle='-', marker='o')

        # Top 3 Mean line
        ax.plot(top_3_means, label="Top 3 Mean", color="red", linestyle='-', marker='x')

        # Title and labels
        ax.set_title("Mean and Top 3 Mean Values Over Time")
        ax.set_xlabel("Time")
        ax.set_ylabel("Value")
        ax.legend()

    # Matplotlib figure and axes
    fig, ax = plt.subplots(figsize=(10, 6))

    # Start the animation
    ani = FuncAnimation(fig, update_graph, interval=1000, cache_frame_data=False)

    plt.tight_layout()
    plt.show()