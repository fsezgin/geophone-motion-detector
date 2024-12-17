import json
import paho.mqtt.client as mqtt
import pandas as pd
from functions.visualization import create_real_time_plot
from functions.data_processing import calculate_statistics, process_and_save_data  # Yeni fonksiyonları ekledik
import time

# Data lists to hold 10-second window data
means = []
top_3_means = []
mins = []
maxs = []
std_devs = []
medians = []
q1s = []
q3s = []
timestamps = []  # Time tracking for CSV export

# 10 saniyelik periyot için veri tutma
window_size = 10  # 10 seconds

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe("geoscope/node1/GEOSCOPE")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    try:
        # Decode the message payload as JSON
        payload = json.loads(msg.payload.decode('utf-8'))
        # Extract the "data" part
        data = payload.get("data", [])

        # Calculate statistical values
        stats = calculate_statistics(data)

        # Append values to respective lists
        means.append(stats["mean"])
        top_3_means.append(stats["top_3_mean"])
        mins.append(stats["min"])
        maxs.append(stats["max"])
        std_devs.append(stats["std_dev"])
        medians.append(stats["median"])
        q1s.append(stats["q1"])
        q3s.append(stats["q3"])

        # Append timestamp for each message received
        current_time = time.strftime("%H:%M:%S")
        timestamps.append(current_time)

        # Print the current time for easier tracking
        print(f"{current_time}, Statistics: {stats}")  # İstatistiksel değerler ve zaman

        # If we've accumulated 10 seconds worth of data, process it
        if len(means) == window_size:
            process_and_save_data(means, top_3_means, mins, maxs, std_devs, medians, q1s, q3s, timestamps)

    except json.JSONDecodeError as e:
        print("JSON decode error:", e)
    except Exception as e:
        print("Error:", e)

# MQTT client
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect("192.168.1.119", 1883, 60)

# Start the MQTT loop
mqttc.loop_start()

# Real-time plot (optional)
create_real_time_plot(means, top_3_means)  # Call the function