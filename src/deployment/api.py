import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import tensorflow as tf
import os
import json
from datetime import datetime

# Load model once at startup
model = tf.keras.models.load_model("models_tff/baseline_central_model.keras")

app = FastAPI(title="Health Risk Prediction API")

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
PRED_LOG_PATH = os.path.join(LOG_DIR, "api_predictions.jsonl")


def log_prediction(payload: dict, prediction: int, raw_output: list):
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "input": payload,
        "prediction": prediction,
        "raw_output": raw_output,
    }
    with open(PRED_LOG_PATH, "a") as f:
        f.write(json.dumps(record) + "\n")


class InputData(BaseModel):
    HeartRate: float
    Temp: float
    PM25: float
    NO2: float
    CO_Level: float


@app.post("/predict")
def predict(data: InputData):
    x = np.array([[data.HeartRate, data.Temp, data.PM25, data.NO2, data.CO_Level]])
    pred = model.predict(x)[0]
    predicted_class = int(np.argmax(pred))
    raw = pred.tolist()

    # Log for monitoring
    log_prediction(data.dict(), predicted_class, raw)

    return {"prediction": predicted_class, "raw_output": raw}


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
