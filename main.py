import json
import paho.mqtt.client as mqtt
from functions.visualization import create_real_time_plot
from functions.data_processing import top_3_avg, calculate_statistics  # İstatistik hesaplama fonksiyonunu ekledik

# Data lists
means = []
top_3_means = []

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

        # Append mean and top_3_mean values to respective lists
        means.append(stats["mean"])
        top_3_means.append(stats["top_3_mean"])

        # Print the data to the terminal
        print(f"Statistics: {stats}")  # İstatistiksel değerler

    except json.JSONDecodeError as e:
        print("JSON decode error:", e)
    except Exception as e:
        print("Error:", e)

# MQTT client
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect("192.168.1.119", 1883, 60)

# Create and display the real-time graph
mqttc.loop_start()  # Start listening to MQTT
create_real_time_plot(means, top_3_means)  # Call the function
