import pandas as pd
import numpy as np
from scipy.stats import skew


# Function to calculate the top 3 peak average
def top_3_avg(data):
    """
    Calculate the average of the top 3 highest values from the dataset.

    Args:
        data (list or array-like): The input dataset.

    Returns:
        float: The average of the top 3 highest values.
    """
    top_3 = sorted(data, reverse=True)[:3]
    top_3_mean = sum(top_3) / len(top_3)
    return top_3_mean


# Function to calculate the dominant frequency using FFT
def dominant_frequency(data):
    """
    Calculate the dominant frequency based on the Fourier Transform of the data.

    Args:
        data (list or array-like): The input dataset.

    Returns:
        float: The dominant frequency in Hertz (Hz).
    """
    # Apply FFT to the data
    fft_result = np.fft.fft(data)

    # Compute frequencies (ensure no frequencies exceed the Nyquist frequency)
    freqs = np.fft.fftfreq(len(fft_result), 1 / 1500)

    # Calculate the magnitudes of the FFT components
    magnitude = np.abs(fft_result)

    # Only consider the positive frequencies and their corresponding magnitudes
    positive_freqs = freqs[:len(freqs) // 2]
    positive_magnitude = magnitude[:len(magnitude) // 2]

    # Identify the index of the frequency with the highest magnitude (ignore DC component)
    peak_idx = np.argmax(positive_magnitude[1:]) + 1  # Skip the DC component at index 0
    dominant_freq = np.abs(positive_freqs[peak_idx])

    return dominant_freq


# Function to calculate the energy of the signal
def signal_energy(data):
    """
    Calculate the energy of the signal. The energy is the sum of the squared values of the data.

    Args:
        data (list or array-like): The input dataset.

    Returns:
        float: The total energy of the signal.
    """
    return np.sum(np.square(data))


# Function to calculate various statistical metrics for the dataset
def calculate_statistics(data):
    """
    Calculate several statistical measures for the given dataset.

    Args:
        data (list or array-like): The input dataset.

    Returns:
        dict: A dictionary containing the calculated statistics (mean, top 3 peak mean, min, max, std dev,
              median, skewness, dominant frequency, and signal energy).
    """
    # Mean value of the data
    mean_value = np.mean(data)

    # Top 3 peak average
    top_3_mean = top_3_avg(data)

    # Minimum and Maximum values
    min_value = np.min(data)
    max_value = np.max(data)

    # Standard deviation
    std_dev = np.std(data)

    # Median value
    median_value = np.median(data)

    # Quartiles (25th and 75th percentiles)
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)

    # Skewness (measuring asymmetry of the distribution)
    skew_value = skew(data)

    # Dominant frequency based on FFT
    dominant_freq_value = dominant_frequency(data)

    # Signal energy (sum of squared values)
    energy = signal_energy(data)

    # Return the calculated statistics as a dictionary
    return {
        "mean": mean_value,
        "top_3_mean": top_3_mean,
        "min": min_value,
        "max": max_value,
        "std_dev": std_dev,
        "median": median_value,
        "q1": q1,
        "q3": q3,
        "skewness": skew_value,
        "dominant_freq": dominant_freq_value,
        "energy": energy
    }


# Function to process the 10-second data window and save to a CSV file
def process_and_save_data(means, top_3_means, mins, maxs, std_devs, medians, q1s, q3s, skewness_vals, dominant_freqs,
                          energies, timestamps):
    """
    Process and save the statistics for the 10-second data window to a CSV file.

    Args:
        means (list): List of mean values.
        top_3_means (list): List of top 3 mean values.
        mins (list): List of minimum values.
        maxs (list): List of maximum values.
        std_devs (list): List of standard deviations.
        medians (list): List of median values.
        q1s (list): List of first quartile values.
        q3s (list): List of third quartile values.
        skewness_vals (list): List of skewness values.
        dominant_freqs (list): List of dominant frequency values.
        energies (list): List of signal energy values.
        timestamps (list): List of timestamps for the data window.

    Saves:
        A CSV file containing the processed statistics for each 10-second window.
    """
    # Create a dictionary to store the processed data to save
    data_to_save = {
        "timestamp": timestamps[-1],  # Save the timestamp of the last data point in the window
        "mean": sum(means) / len(means),
        "top_3_mean": sum(top_3_means) / len(top_3_means),
        "min": min(mins),
        "max": max(maxs),
        "std_dev": sum(std_devs) / len(std_devs),
        "median": sum(medians) / len(medians),
        "q1": sum(q1s) / len(q1s),
        "q3": sum(q3s) / len(q3s),
        "skewness": sum(skewness_vals) / len(skewness_vals),
        "dominant_freq": sum(dominant_freqs) / len(dominant_freqs),
        "energy": sum(energies) / len(energies)
    }

    # Convert the dictionary to a DataFrame and append it to a CSV file
    df = pd.DataFrame([data_to_save])
    df.to_csv("data/processed_data.csv", mode='a', header=not pd.io.common.file_exists("data/processed_data.csv"),
              index=False)

    # Reset the lists for the next 10-second data window
    means.clear()
    top_3_means.clear()
    mins.clear()
    maxs.clear()
    std_devs.clear()
    medians.clear()
    q1s.clear()
    q3s.clear()
    skewness_vals.clear()
    dominant_freqs.clear()
    energies.clear()
    timestamps.clear()
