import joblib
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

# Загружаем модель, scaler и список признаков
model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")
features = joblib.load("features.pkl")  # Загрузка признаков из файла

app = FastAPI()

class InputData(BaseModel):
    data: List[float]

@app.get("/")
def root():
    return {"message": "Модель работает!", "model_type": str(type(model)), "num_features": len(features)}

@app.post("/predict")
def predict(input_data: InputData):
    if len(input_data.data) != len(features):
        return {"error": f"Ожидается {len(features)} признаков, получено {len(input_data.data)}."}

    try:
        X = np.array(input_data.data).reshape(1, -1)
        X_scaled = scaler.transform(X)
        prediction = model.predict(X_scaled)[0]
        return {"predicted_physicalactivity_min": round(float(prediction), 2)}
    
    except Exception as e:
        return {"error": str(e)}
