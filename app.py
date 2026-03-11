from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import os

app = Flask(__name__)
# Enable Cross-Origin Resource Sharing so the frontend can call this API
CORS(app)

# Load the trained model
MODEL_PATH = 'model/weather_calls_model.pkl'
model = None

if os.path.exists(MODEL_PATH):
    try:
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
    except Exception as e:
        print(f"Error loading model: {e}")
else:
    print("Warning: Model file not found. Please run train_model.py first.")

@app.route('/api/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({"error": "Model not loaded on server."}), 500
        
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON payload received"}), 400
        
    try:
        weather_list = data.get('weather_data', [])
        if not weather_list:
            return jsonify({"error": "Empty weather_data record"}), 400

        predictions = []
        baselines = []
        
        for item in weather_list:
            # Safely extract and convert features
            try:
                hour = float(item.get('hour', 12))
                temp = float(item.get('temperature', 30))
                humidity = float(item.get('humidity', 60))
                wind = float(item.get('wind_speed', 10))
                rain = float(item.get('rain_prob', 0))
                
                # Create feature array
                features = np.array([[hour, temp, humidity, wind, rain]])
                
                # Predict using the loaded model
                raw_pred = model.predict(features)[0]
                pred_volume = int(raw_pred)
                predictions.append(pred_volume)
                
                # Calculate simple baseline
                base_load = int(200 + 150 * max(0, min(1, np.sin(np.pi * (hour - 6) / 12))))
                baselines.append(base_load)
            except (ValueError, TypeError) as ve:
                print(f"Skipping invalid data point: {ve}")
                continue
            
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
    # Using 8000 as fallback if 5000 is jammed, but keeping 5000 per user request
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
