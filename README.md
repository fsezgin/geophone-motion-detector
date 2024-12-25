# README: Activity and User Analysis using Geosphone Sensor Data

## Project Overview
This project utilizes a geoscope sensor to analyze human activities (walking, running, standing still) and identify individuals based on their activity patterns. The sensor provides vibration data as numerical values at a sampling rate of 500 Hz. These data are processed and used to train a Long Short-Term Memory (LSTM) model for classification tasks.

### Objectives
1. **Activity Analysis**: Classify activities into three categories: walking, running, and standing still.
2. **Activity and User Identification**: Expand the classification to include user identification along with the activity type (e.g., User A walking).

---

## Features Used
The features extracted from the vibration data can be divided into **statistical** and **frequency-domain** categories:

### Statistical Features (calculated per time window):
1. **Mean**: Average value of the signal.
2. **Median**: Middle value of the signal.
3. **Standard Deviation (std_dev)**: Measure of signal dispersion.
4. **Minimum (min)**: Lowest signal value.
5. **Maximum (max)**: Highest signal value.
6. **First Quartile (Q1)**: Median of the lower half of the data.
7. **Third Quartile (Q3)**: Median of the upper half of the data.
8. **Skewness**: Symmetry of the signal distribution.

### Frequency-Domain Features (calculated using Fourier Transform):
1. **Dominant Frequency**: Frequency with the highest power.
2. **Signal Energy**: Total power of the signal.
---

## Workflow
### Data Collection
1. Sensor data is streamed via MQTT.
2. Data is collected in real time, segmented into 3-second time windows (or configurable).
3. Each window generates one set of feature values for training/testing the model.

### Data Processing
1. Raw sensor data is passed through a **band-pass filter** (0.5-50 Hz) to remove noise and irrelevant frequencies.
2. Statistical and frequency-domain features are extracted for each time window.
3. Features and labels are saved into a structured dataset (CSV format).

### Model Training
- **Model Type**: Long Short-Term Memory (LSTM)
- **Input**: Feature values extracted from 3-second windows.
- **Output**: Predicted activity or activity + user label.
- **Dataset Split**: 70% training, 15% validation, 15% testing.

### Model Evaluation
Key metrics for evaluating the classification model:
1. **Accuracy**: Overall correctness of the predictions.
2. **Precision**: Proportion of true positive predictions.
3. **Recall**: Proportion of actual positives correctly identified.
4. **F1-Score**: Harmonic mean of precision and recall.
5. **Confusion Matrix**: Visual representation of true vs. predicted labels.

---

## Key Results
Example classification results for activity analysis:
- **Accuracy**: ~88%
- **Confusion Matrix**: Shows distinct separability for activities like running and standing still, with minor misclassifications in walking.

---

## Installation
1. Clone this repository.
   ```bash
   git clone https://github.com/fsezgin/geoscope-motion-detector.git
   cd fsezgin/geoscope-motion-detector
   ```
2. Install the required dependencies.
   ```bash
   pip install -r requirements.txt
   ```
3. Configure the MQTT client in `main.py` to connect to your sensor's server.

---

## Usage
1. **Run the data collection pipeline:**
   ```bash
   python main.py
   ```
   This script will collect sensor data, process it into features, and save it to a CSV file.
---

## Folder Structure
```
project/
|-- data/
|   |-- processed_data.csv  # Feature-processed data
|
|-- functions/
|   |-- data_processing.py  # Feature extraction methods
|   |-- visualization.py    # Real-time and static visualization
|
|-- models/
|   |-- lstm_model.py       # Model architecture
|
|-- main.py                 # Main data collection script
|-- requirements.txt        # Python dependencies
```

## Contributors
- **Furkan Sezgin**: Project lead and developer.
