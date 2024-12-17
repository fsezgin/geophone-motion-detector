import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def create_real_time_plot(means, top_3_means):
    """
    Gerçek zamanlı veri çizimi için bir grafik oluşturur.

    Args:
        means (list): Ortalama değerlerin listesi.
        top_3_means (list): Top 3 ortalama değerlerin listesi.
    """

    def update_graph(frame):
        ax.clear()

        # Ortalama çizgisi
        ax.plot(means, label="Mean", color="blue", linestyle='-', marker='o')

        # Top 3 Ortalama çizgisi
        ax.plot(top_3_means, label="Top 3 Mean", color="red", linestyle='-', marker='x')

        # Başlık ve etiketler
        ax.set_title("Mean and Top 3 Mean Values Over Time")
        ax.set_xlabel("Time")
        ax.set_ylabel("Value")
        ax.legend()

    # Matplotlib figür ve eksen
    fig, ax = plt.subplots(figsize=(10, 6))

    # Animasyonu başlat
    ani = FuncAnimation(fig, update_graph, interval=1000, cache_frame_data=False)

    plt.tight_layout()
    plt.show()