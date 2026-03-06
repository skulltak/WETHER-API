from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import datetime
import os

app = Flask(__name__)
# Enable Cross-Origin Resource Sharing so the frontend can call this API
CORS(app)

# Load the trained model
MODEL_PATH = 'model/weather_calls_model.pkl'
if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
else:
    print("Warning: Model file not found. Please run train_model.py first.")
    model = None

@app.route('/api/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({"error": "Model not loaded on server."}), 500
        
    try:
        data = request.json
        print("Received Prediction Request:", data)
        
        # Expected input format:
        # { "weather_data": [
        #   {"hour": 8, "temperature": 25, "humidity": 60, "wind_speed": 10, "rain_prob": 0},
        #   {"hour": 10, "temperature": 28, "humidity": 55, "wind_speed": 12, "rain_prob": 5}, ...
        # ]}
        
        predictions = []
        baselines = []
        
        for item in data.get('weather_data', []):
            hour = float(item.get('hour', 12))
            temp = float(item.get('temperature', 30))
            humidity = float(item.get('humidity', 60))
            wind = float(item.get('wind_speed', 10))
            rain = float(item.get('rain_prob', 0))
            
            # Create feature array matching training data order
            # ['hour', 'temperature', 'humidity', 'wind_speed', 'rain_prob']
            features = np.array([[hour, temp, humidity, wind, rain]])
            
            # Predict using the loaded Random Forest model
            pred_volume = int(model.predict(features)[0])
            predictions.append(pred_volume)
            
            # Calculate a simple baseline (derived from earlier synthetic logic)
            base_load = int(200 + 150 * max(0, min(1, np.sin(np.pi * (hour - 6) / 12))))
            baselines.append(base_load)
            
        return jsonify({
            "status": "success",
            "predictions": predictions,
            "baselines": baselines
        })
        
    except Exception as e:
        print("Prediction Error:", str(e))
        return jsonify({"error": str(e)}), 400

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "model_loaded": model is not None})

if __name__ == '__main__':
    print("Starting VECARE ML Backend Server on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=True)
