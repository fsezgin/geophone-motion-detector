import numpy as np

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