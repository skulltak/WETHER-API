import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import pickle
import os

# 1. Generate Synthetic Data
def generate_data(n=5000):
    np.random.seed(42)
    
    # Generate features
    hours = np.random.randint(0, 24, n)
    temps = np.random.normal(30, 8, n) # Mean 30C, SD 8
    humidity = np.random.normal(60, 20, n).clip(10, 100)
    wind_speed = np.random.exponential(10, n).clip(0, 80)
    rain_prob = np.random.exponential(15, n).clip(0, 100)
    
    # Base load determined by time of day
    base_load = 200 + 150 * np.sin(np.pi * (hours - 6) / 12).clip(0, 1)
    
    # Add weather impacts
    rain_impact = np.where(rain_prob > 50, (rain_prob - 50) * 8, rain_prob * 0.5)
    temp_impact = np.where(temps > 35, (temps - 35) * 5, 0)
    wind_impact = np.where(wind_speed > 30, (wind_speed - 30) * 4, 0)
    
    # Calculate total call volume with noise
    call_volume = base_load + rain_impact + temp_impact + wind_impact + np.random.normal(0, 20, n)
    call_volume = np.maximum(50, call_volume).astype(int) 
    
    return pd.DataFrame({
        'hour': hours,
        'temperature': temps,
        'humidity': humidity,
        'wind_speed': wind_speed,
        'rain_prob': rain_prob,
        'call_volume': call_volume
    })

def train():
    print("Generating synthetic weather telemetry...")
    df = generate_data()
    
    # 2. Train the Model
    X = df[['hour', 'temperature', 'humidity', 'wind_speed', 'rain_prob']]
    y = df['call_volume']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print(f"Training RandomForest model on {len(X_train)} samples...")
    model = RandomForestRegressor(n_estimators=100, max_depth=15, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print("\n--- Model Metrics ---")
    print(f"RMSE: {rmse:.2f}")
    print(f"MAE:  {mae:.2f}")
    print(f"R2 :  {r2:.4f}")
    
    # 3. Save the Model
    os.makedirs('model', exist_ok=True)
    with open('model/weather_calls_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    print("\nModel saved to model/weather_calls_model.pkl")

if __name__ == '__main__':
    train()
