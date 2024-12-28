import numpy as np
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf

scaler = MinMaxScaler()

def preprocess_data(df, time_steps):
    """
    Veri ön işleme ve zaman dilimleri oluşturma.
    """
    # Sayısal sütunları seç
    numeric_columns = df.select_dtypes(include=["float64", "int64"]).columns

    # Veriyi ölçeklendirme
    features_scaled = scaler.fit_transform(df[numeric_columns])

    # Zaman dilimlerini oluştur
    X = create_sequences(features_scaled, time_steps)
    return X

def create_sequences(features_scaled, time_steps=3):
    """
    Zaman dilimleri oluşturma.
    """
    X = []
    for i in range(len(features_scaled) - time_steps):
        X.append(features_scaled[i:i + time_steps])
    return np.array(X)

def make_predict(df, time_steps, model_path):
    """
    Model ile tahmin yapma.
    """
    # Veri ön işleme
    X_given = preprocess_data(df, time_steps)

    # Modeli yükle
    model = tf.keras.models.load_model(model_path)

    # Tahmin yap
    y_pred = np.argmax(model.predict(X_given), axis=1)
    return y_pred




