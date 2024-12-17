import numpy as np
import pandas as pd

# Top 3 peak average
def top_3_avg(data):
    top_3 = sorted(data, reverse=True)[:3]
    top_3_mean = sum(top_3) / len(top_3)
    return top_3_mean

def calculate_statistics(data):
    """
    Calculate various statistical metrics for a given dataset.

    Args:
        data (list or array-like): The input dataset.

    Returns:
        dict: A dictionary containing the calculated statistics.
    """

    # Average of the top 3 peaks
    top_3_mean = top_3_avg(data)

    # Mean
    mean_value = np.mean(data)

    # Minimum and Maximum
    min_value = np.min(data)
    max_value = np.max(data)

    # Standard Deviation
    std_dev = np.std(data)

    # Median
    median_value = np.median(data)

    # Quartiles (Q1 and Q3)
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)

    # Return the statistics
    return {
        "mean": mean_value,
        "top_3_mean": top_3_mean,
        "min": min_value,
        "max": max_value,
        "std_dev": std_dev,
        "median": median_value,
        "q1": q1,
        "q3": q3
    }

# Process the 10-second data and save to CSV
# Process the 10-second data and save to CSV
def process_and_save_data(means, top_3_means, mins, maxs, std_devs, medians, q1s, q3s, timestamps):
    """
    Processes the 10-second window data and appends the statistics to a CSV file.
    """
    # Create a dictionary with the data to save
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
    }

    # Convert data to DataFrame and append to CSV file
    df = pd.DataFrame([data_to_save])
    df.to_csv("data/processed_data.csv", mode='a', header=not pd.io.common.file_exists("data/processed_data.csv"), index=False)

    # Clear the lists for the next 10-second window
    means.clear()
    top_3_means.clear()
    mins.clear()
    maxs.clear()
    std_devs.clear()
    medians.clear()
    q1s.clear()
    q3s.clear()
    timestamps.clear()