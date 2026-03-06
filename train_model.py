import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pickle
import os

# 1. Generate Synthetic Data
# Let's create a dataset where call volume is influenced by:
# - Temperature (higher temp in summer -> maybe more calls)
# - Rain (heavy rain -> significantly more calls)
# - Wind Speed (very high wind -> more calls)
# - Humidity (moderate impact)
# - Hour of day (peak hours)

np.random.seed(42)
num_samples = 5000

# Generate features
hours = np.random.randint(0, 24, num_samples)
temps = np.random.normal(30, 8, num_samples) # Mean 30C, SD 8
humidity = np.random.normal(60, 20, num_samples).clip(10, 100)
wind_speed = np.random.exponential(10, num_samples).clip(0, 80)
rain_prob = np.random.exponential(15, num_samples).clip(0, 100)

# Base load determined by time of day (sine wave peaking around noon)
base_load = 200 + 150 * np.sin(np.pi * (hours - 6) / 12).clip(0, 1)

# Add weather impacts
# Rain has a massive impact if it's high
rain_impact = np.where(rain_prob > 50, (rain_prob - 50) * 8, rain_prob * 0.5)
# Temp impact (extreme heat causing more calls)
temp_impact = np.where(temps > 35, (temps - 35) * 5, 0)
# Wind impact
wind_impact = np.where(wind_speed > 30, (wind_speed - 30) * 4, 0)

# Calculate total call volume with some random noise
call_volume = base_load + rain_impact + temp_impact + wind_impact + np.random.normal(0, 20, num_samples)
call_volume = np.maximum(50, call_volume).astype(int) # Minimum 50 calls

# Create DataFrame
df = pd.DataFrame({
    'hour': hours,
    'temperature': temps,
    'humidity': humidity,
    'wind_speed': wind_speed,
    'rain_prob': rain_prob,
    'call_volume': call_volume
})

# 2. Train the Model
X = df[['hour', 'temperature', 'humidity', 'wind_speed', 'rain_prob']]
y = df['call_volume']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Training RandomForest model...")
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
predictions = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, predictions))
print(f"Model trained successfully! RMSE: {rmse:.2f}")

# 3. Save the Model
os.makedirs('model', exist_ok=True)
with open('model/weather_calls_model.pkl', 'wb') as f:
    pickle.dump(model, f)
print("Model saved to model/weather_calls_model.pkl")
