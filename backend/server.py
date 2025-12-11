
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import joblib
import pandas as pd
import json
import os
import uvicorn

app = FastAPI(title="Wine Quality API", description="Backend for Wine Quality Prediction")

# CORS Configuration
# CORS Configuration
# Allow all origins for production deployment ease (or restrict to Vercel domain later)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Model and Artifacts
MODEL_PATH = "best_model_wine_quality.joblib"
FEATURES_PATH = "feature_names.json"
METRICS_PATH = "metrics.json"

class PredictionRequest(BaseModel):
    features: dict

@app.get("/")
def read_root():
    return {"message": "Welcome to the Wine Quality Prediction API"}

@app.get("/features")
def get_features():
    if not os.path.exists(FEATURES_PATH):
        # Fallback if file not found (e.g. before training)
        return {"features": []}
    with open(FEATURES_PATH, "r") as f:
        features = json.load(f)
    return {"features": features}

@app.get("/metrics")
def get_metrics():
    if not os.path.exists(METRICS_PATH):
        return {"error": "Metrics not found"}
    with open(METRICS_PATH, "r") as f:
        metrics = json.load(f)
    return metrics

@app.post("/predict")
def predict_quality(request: PredictionRequest):
    if not os.path.exists(MODEL_PATH):
        raise HTTPException(status_code=503, detail="Model not loaded. Please train the model first.")
    
    try:
        model = joblib.load(MODEL_PATH)
        # Convert input dict to DataFrame
        # Ensure correct order if feature_names is available
        if os.path.exists(FEATURES_PATH):
             with open(FEATURES_PATH, "r") as f:
                feature_order = json.load(f)
             # Create DF ensuring column order
             data = {k: [v] for k, v in request.features.items()}
             df = pd.DataFrame(data)
             # Fill missing cols with 0 or handle error? 
             # For now assume frontend sends all needed keys or we reindex
             df = df.reindex(columns=feature_order, fill_value=0)
        else:
             # Just use what is sent
             df = pd.DataFrame([request.features])

        prediction = model.predict(df)[0]
        score = round(float(prediction), 1)

        # Advisor Logic
        if score >= 7.5:
            verdict = "Exceptional Vintage"
            advice = "This wine shows outstanding complexity and balance. A truly superior choice suitable for aging."
        elif score >= 6.0:
            verdict = "Fine Table Wine"
            advice = "A solid, enjoyable wine with good character. Perfect for daily consumption or casual dining."
        else:
            verdict = "Below Average"
            advice = "This wine may have noticeable flaws or lacks balance. Might be best used for cooking or sangria."

        return {
            "score": score,
            "verdict": verdict,
            "advice": advice
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/report")
def get_report():
    report_path = "Wine_Quality_Report.md"
    if not os.path.exists(report_path):
        return {"content": "# Report not found\nPlease run `generate_report.py`."}
    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()
    return {"content": content}

@app.get("/eda/{image_name}")
def get_eda_image(image_name: str):
    # Security check: only allow known pngs
    allowed_images = ["eda_histograms.png", "eda_correlation.png", "eda_quality_dist.png"]
    if image_name not in allowed_images:
        raise HTTPException(status_code=404, detail="Image not found")
    
    if not os.path.exists(image_name):
        raise HTTPException(status_code=404, detail="Image file not generated yet")
    
    return FileResponse(image_name)

#if __name__ == "__main__":
#  uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
