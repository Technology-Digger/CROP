#
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import numpy as np
from pathlib import Path

# Paths to your saved models
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR.parent / "models" / "model.pkl"
MINMAX_PATH = BASE_DIR.parent / "models" / "minmaxscaler.pkl"
STAND_PATH = BASE_DIR.parent / "models" / "standscaler.pkl"

# Load model and scalers
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

with open(MINMAX_PATH, "rb") as f:
    minmax_scaler = pickle.load(f)

with open(STAND_PATH, "rb") as f:
    stand_scaler = pickle.load(f)

# FastAPI app
app = FastAPI(title="EcoCrop Backend")

# Allow frontend (Vite) to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input model
class InputData(BaseModel):
    N: float
    P: float
    K: float
    ph: float
    rainfall: float
    temperature: float
    humidity: float

# Map model numbers to crop names
num_to_crop = {
    1: 'Rice', 2: 'Maize', 3: 'Jute', 4: 'Cotton', 5: 'Coconut',
    6: 'Papaya', 7: 'Orange', 8: 'Apple', 9: 'Muskmelon', 10: 'Watermelon',
    11: 'Grapes', 12: 'Mango', 13: 'Banana', 14: 'Pomegranate', 15: 'Lentil',
    16: 'Blackgram', 17: 'Mungbean', 18: 'Mothbeans', 19: 'Pigeonpeas',
    20: 'Kidneybeans', 21: 'Chickpea', 22: 'Coffee'
}


@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "Backend running 🚀"}

@app.post("/api/predict")
def predict(data: InputData):
    try:
        features = np.array([[
            data.N,
            data.P,
            data.K,
            data.ph,
            data.rainfall,
            data.temperature,
            data.humidity,
        ]])
        x_scaled = minmax_scaler.transform(features)
        x_scaled = stand_scaler.transform(x_scaled)
        prediction = model.predict(x_scaled)
        
        # Convert numeric prediction to crop name
        crop_name = num_to_crop.get(prediction[0], "Unknown crop")
        return {"prediction": crop_name}
    
    except Exception as e:
        return {"error": str(e)}
