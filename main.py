import json
import paho.mqtt.client as mqtt
from functions.visualization import create_real_time_plot
from functions.data_processing import preprocess_data

# Veri listeleri
means = []
top_3_means = []

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe("geoscope/node1/GEOSCOPE")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    try:
        # Mesaj yükünü JSON olarak çözümle
        payload = json.loads(msg.payload.decode('utf-8'))
        # "data" kısmını al
        data = payload.get("data", [])

        # Veriyi işle ve tüm veri için mean ve top 3 mean değerlerini al
        mean_value, top_3_mean = preprocess_data(data)

        # Ortalama ve top 3 ortalamayı ekle
        means.append(mean_value)
        top_3_means.append(top_3_mean)

        # Veriyi terminale yazdır
        print(f"Mean: {mean_value}, Top 3 Mean: {top_3_mean}")
        print("hello")

    except json.JSONDecodeError as e:
        print("JSON decode error:", e)
    except Exception as e:
        print("Error:", e)

# MQTT client
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect("192.168.1.119", 1883, 60)

# Gerçek zamanlı grafiği oluştur ve göster
mqttc.loop_start()  # MQTT dinlemeyi başlat
create_real_time_plot(means, top_3_means)  # Fonksiyonu çağır
