import joblib
import sys

try:
    print("Loading model...")
    model = joblib.load("best_model_wine_quality.joblib")
    print("Model loaded successfully.")
    print(f"Model type: {type(model)}")
except Exception as e:
    print(f"ERROR: {e}")
    # Print full traceback
    import traceback
    traceback.print_exc()
