import json
import os

import paho.mqtt.client as mqtt
import pandas as pd
import numpy as np
from helpers.feature_extraction import calculate_statistics, process_and_save_data
from helpers.visualization import create_real_time_plot
from tensorflow.python.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

# Load the pre-trained model
model_directory = r'C:\Users\furka\Desktop\ain4311\project\real-time-motion-detector\models'
model_path = os.path.join(model_directory, '3', 'lstm_geophone_sensor_name_predictv2.h5')
model = load_model(model_path)

# Initialize the scaler
scaler = MinMaxScaler()

# Data lists to hold accumulated data for processing
data_list = []  # Holds the incoming data for a specific time window (e.g., 3 seconds)
timestamps = []  # List to track timestamps for saving data in CSV format

# Number of values to collect before processing (for a 3-second window, 3 * 500 = 1500 data points)
timer = 0  # Timer to count how many times the on_message function has been triggered
count = 0

# Real-time data visualization points
point = []

# Function to preprocess real-time data
def preprocess_real_time_data(data, time_steps):
    # Normalize the data
    numeric_columns = ['mean', 'top_3_mean', 'min', 'max', 'std_dev', 'median',
                       'q1', 'q3', 'skewness', 'dominant_freq', 'energy']
    scaled_values = scaler.fit_transform(data[numeric_columns])

    # Create sequences
    sequences = []
    for i in range(len(scaled_values) - time_steps + 1):
        sequences.append(scaled_values[i:i + time_steps])

    return np.array(sequences)

# MQTT callback functions
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe("geoscope/node1/GEOSCOPE")

def on_message(client, userdata, msg):
    global timer, data_list, count

    try:
        # Decode the message payload as JSON
        payload = json.loads(msg.payload.decode('utf-8'))
        data = payload.get("data", [])
        print(f"Received Data: {data}")

        # Append incoming data
        data_list.extend(data)
        timer += 1

        if timer >= 3:  # Process every 3 seconds
            count +=1
            stats = calculate_statistics(data_list)
            print(f"Calculated Statistics: {stats}")

            # Prepare real-time data for prediction
            current_data = pd.DataFrame([stats])
            sequences = preprocess_real_time_data(current_data, time_steps=3)

            if count >= 3:
                # Make predictions
               predictions = model.predict(sequences)
               predicted_label = np.argmax(predictions, axis=1)
               print(f"Predicted Activity: {predicted_label}")

            # Save data
            process_and_save_data(stats, "data/processed_data.csv")

            # Reset timer and data
            data_list.clear()
            timer = 0

    except Exception as e:
        print(f"Error: {e}")

# MQTT client setup
mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.connect("192.168.1.119", 1883, 60)

# Start MQTT loop
mqttc.loop_start()
create_real_time_plot(point)
