import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler

def get_last_n_data(file_path, sequence_length):
    """
    Son 'sequence_length' kadar veriyi CSV dosyasından alır.

    Args:
        file_path (str): CSV dosyasının yolu.
        sequence_length (int): Son alınacak veri sayısı.

    Returns:
        pd.DataFrame: Son 'sequence_length' kadar veriyi içeren DataFrame.
    """
    # CSV dosyasını oku
    data = pd.read_csv(file_path)

    # Son 'sequence_length' kadar veriyi al
    last_n_data = data.tail(sequence_length)

    return last_n_data


def preprocess_data_for_model(last_n_data, scaler=None):
    # Zaman ve aktivite sütunlarını çıkar
    features = last_n_data.drop(columns=['timestamp', 'activity']).values

    # Eğer scaler yoksa, yeni bir scaler oluştur ve veriyi normalleştir
    if scaler is None:
        scaler = MinMaxScaler()
        scaled_features = scaler.fit_transform(features)
    else:
        scaled_features = scaler.transform(features)

    # Modelin beklediği formata getir (1 örnek, 3 zaman adımı, 11 özellik)
    X = scaled_features.reshape(1, scaled_features.shape[0], scaled_features.shape[1])

    return X, scaler


def predict_from_csv(model, file_path, sequence_length=3, label_encoder=None):
    """
    CSV dosyasındaki veriyi kullanarak tahmin yapar.
    """
    # Son sequence_length kadar veriyi al
    last_n_data = get_last_n_data(file_path, sequence_length)

    # Veriyi modele uygun formata getir
    X, scaler = preprocess_data_for_model(last_n_data)

    # Modeli kullanarak tahmin yap
    prediction = model.predict(X)

    # En yüksek olasılığa sahip sınıf etiketini al
    predicted_class_index = np.argmax(prediction, axis=1)

    # Eğer label_encoder varsa, tahmin edilen sınıfı geri dönüştür
    if label_encoder:
        predicted_label = label_encoder.inverse_transform(predicted_class_index)
        return predicted_label[0]

    # Eğer label_encoder yoksa, sadece sınıf indeksini döndür
    return predicted_class_index[0]


def load_trained_model(model_path):
    print("Model yükleniyor...")
    return tf.keras.models.load_model(model_path, compile=False)
