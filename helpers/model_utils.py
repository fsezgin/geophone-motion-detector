import pickle

import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler

def get_last_n_data(file_path, sequence_length):
    """
    Retrieves the last 'sequence_length' number of records from the CSV file.

    Args:
        file_path (str): The path to the CSV file.
        sequence_length (int): The number of recent records to retrieve.

    Returns:
        pd.DataFrame: A DataFrame containing the last 'sequence_length' records.
    """
    # Read the CSV file
    data = pd.read_csv(file_path)

    # Retrieve the last 'sequence_length' records
    last_n_data = data.tail(sequence_length)

    return last_n_data


def preprocess_data_for_model(last_n_data, scaler=None):
    """
    Preprocesses the data to fit the model's expected input format.
    Normalizes the features and reshapes them for the model.

    Args:
        last_n_data (pd.DataFrame): DataFrame containing the most recent data to be used for prediction.
        scaler (MinMaxScaler, optional): Pre-fitted scaler to normalize the features. If None, a new scaler is used.

    Returns:
        np.ndarray: The preprocessed data, reshaped for the model.
        MinMaxScaler: The scaler used for normalization.
    """

    # Drop timestamp and activity columns, as they are not used for prediction
    features = last_n_data.drop(columns=['timestamp', 'activity']).values

    # If no scaler is passed, create a new scaler and fit it to the data
    if scaler is None:
        scaler = MinMaxScaler()
        scaled_features = scaler.fit_transform(features)
    else:
        # If a scaler is provided, use it to scale the data
        scaled_features = scaler.transform(features)

    # Reshape the data to fit the model input format (1 example, 3 time steps, 11 features)
    X = scaled_features.reshape(1, scaled_features.shape[0], scaled_features.shape[1])

    return X, scaler


def predict_from_csv(model, file_path, sequence_length=3, label_encoder_path=None):
    """
    Makes a prediction using the model based on the data from a CSV file.

    Args:
        model (tf.keras.Model): The trained model used for prediction.
        file_path (str): Path to the CSV file containing the data.
        sequence_length (int, optional): The number of recent records to consider for prediction. Default is 3.
        label_encoder_path (str, optional): Path to the label encoder file. If provided, it will be used to map predictions back to labels.

    Returns:
        str or int: The predicted class label or class index, depending on whether the label encoder is provided.
    """
    # Load the label encoder if the path is provided
    label_encoder = None
    if label_encoder_path:
        label_encoder = load_label_encoder(label_encoder_path)

    # Retrieve the last 'sequence_length' records from the CSV
    last_n_data = get_last_n_data(file_path, sequence_length)

    # Preprocess the data to fit the model's input format
    X, scaler = preprocess_data_for_model(last_n_data)

    # Make the prediction using the trained model
    prediction = model.predict(X)

    # Get the index of the class with the highest probability
    predicted_class_index = np.argmax(prediction, axis=1)

    # If a label encoder is provided, map the predicted index back to the class label
    if label_encoder:
        predicted_label = label_encoder.inverse_transform(predicted_class_index)
        return predicted_label[0]

    # If no label encoder is provided, return the class index
    return predicted_class_index[0]


def load_label_encoder(label_encoder_path):
    """
    Loads the label encoder from the specified file path.

    Args:
        label_encoder_path (str): Path to the label encoder file.

    Returns:
        LabelEncoder: The loaded label encoder.
    """
    with open(label_encoder_path, 'rb') as f:
        label_encoder = pickle.load(f)
    return label_encoder

def load_trained_model(model_path):
    """
    Loads the label encoder from the specified file path.

    Args:
        label_encoder_path (str): Path to the label encoder file.

    Returns:
        LabelEncoder: The loaded label encoder.
    """
    print("Loading model...")
    return tf.keras.models.load_model(model_path, compile=False)
