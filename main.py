import json
import paho.mqtt.client as mqtt
import numpy as np

import time

from helpers.feature_extraction import calculate_statistics, process_and_save_data
from helpers.model_utils import load_trained_model, predict_from_csv
from helpers.visualization import create_real_time_plot

# Data lists to hold accumulated data for processing
data_list = []  # Holds the incoming data for a specific time window (e.g., 3 seconds)
timestamps = []  # List to track timestamps for saving data in CSV format

# The number of values to collect before processing (for a 3-second window, 3 * 500 = 1500 data points)
timer = 0  # Timer to count how many times the on_message function has been triggered
count = 0
# A list to hold the per-second averages for real-time plotting
point = []

# Load the trained model and label encoder path
model = load_trained_model(r'C:\Users\furka\Desktop\ain4311\project\real-time-motion-detector\models\2\fs_model_lstm_v5.h5')
label_encoder_path = r'C:\Users\furka\Desktop\ain4311\project\real-time-motion-detector\config\label_encoder.pkl'


# Callback function when the client connects to the MQTT server
def on_connect(client, userdata, flags, reason_code, properties):
    """
    Called when the client successfully connects to the broker.

    Args:
        client (mqtt.Client): The MQTT client instance.
        userdata (any): The private user data (if any).
        flags (dict): Connection flags (if any).
        reason_code (int): The reason code for the connection.
        properties (dict): Connection properties (if any).
    """
    print(f"Connected with result code {reason_code}")
    # Subscribe to the desired topic to start receiving messages
    client.subscribe("geoscope/node1/GEOSCOPE")


# Callback function when a PUBLISH message is received from the server
def on_message(client, userdata, msg):
    """
    Called when a message is received on a subscribed topic.

    Args:
        client (mqtt.Client): The MQTT client instance.
        userdata (any): The private user data (if any).
        msg (mqtt.MQTTMessage): The received message containing the payload and topic.
    """
    global timer  # Use the global timer variable to keep track of message count
    global count

    try:
        # Decode the message payload as JSON
        payload = json.loads(msg.payload.decode('utf-8'))
        # Extract the "data" part from the payload
        data = payload.get("data", [])

        # Print the received data for debugging
        print(f"Received Data: {data}")

        # Append all incoming data points to the data_list
        data_list.extend(data)

        # Calculate the per-second average (point) and append it to the list for real-time plotting
        point.append(np.mean(data))

        # Increment the timer each time a message is received
        timer += 1


        # If the timer has reached 3, process the statistics for the 3-second window
        if timer == 3:
            count +=1
            print(count)
            # Perform statistical calculations for the data window
            stats = calculate_statistics(data_list)

            # Extract individual statistics for further processing
            means = [stats["mean"]]
            top_3_means = [stats["top_3_mean"]]
            mins = [stats["min"]]
            maxs = [stats["max"]]
            std_devs = [stats["std_dev"]]
            medians = [stats["median"]]
            q1s = [stats["q1"]]
            q3s = [stats["q3"]]
            skewness_vals = [stats["skewness"]]
            dominant_freqs = [stats["dominant_freq"]]
            energies = [stats["energy"]]

            # Print the statistics for tracking and debugging
            print(f"Statistics for window: {stats}")

            # Store the current timestamp for data logging
            current_time = time.strftime("%H:%M:%S")
            timestamps.append(current_time)  # Store the timestamp of the current window

            # Process and save the calculated statistics to a CSV file
            process_and_save_data(means, top_3_means, mins, maxs, std_devs, medians, q1s, q3s, skewness_vals,
                                  dominant_freqs, energies, timestamps)

            if count >= 9: # After processing enough data, make predictions (3 * 3-second windows)
                predictions_inverse = predict_from_csv(model, r"C:\Users\furka\Desktop\ain4311\project\real-time-motion-detector\data\processed_data.csv", sequence_length=3, label_encoder_path=label_encoder_path)
                print(f"Predictions: {predictions_inverse}")

            # Clear the data list for the next window of incoming data
            data_list.clear()
            timer = 0  # Reset the timer after processing the current window

    except json.JSONDecodeError as e:
        # Handle JSON decoding errors gracefully
        print("JSON decode error:", e)
    except Exception as e:
        # Catch any other unexpected errors and print them
        print("Error:", e)


# MQTT client setup
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)  # Initialize the MQTT client with the appropriate version
mqttc.on_connect = on_connect  # Set the callback for successful connection
mqttc.on_message = on_message  # Set the callback for incoming messages

# Connect to the MQTT broker at the specified IP address and port
mqttc.connect("192.168.1.119", 1883, 60)

# Start the MQTT loop to handle incoming messages
mqttc.loop_start()

# Real-time plotting (optional) - Using the list 'A' to track the per-second average for plotting
create_real_time_plot(point)  # Call the real-time plot function with the 'A' variable to display averages