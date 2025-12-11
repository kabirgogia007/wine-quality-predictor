import joblib
import pandas as pd
import traceback
import numpy as np
import sklearn

print(f"Numpy version: {np.__version__}")
print(f"Sklearn version: {sklearn.__version__}")

try:
    print("Loading model...")
    model = joblib.load("best_model_wine_quality.joblib")
    
    print("Preparing input...")
    # Create dummy input similar to what valid prediction would request
    # Need 11 features
    features = ['fixed_acidity','volatile_acidity','citric_acid','residual_sugar',
                'chlorides','free_sulfur_dioxide','total_sulfur_dioxide','density',
                'pH','sulphates','alcohol']
    data = {f: [0.5] for f in features}
    df = pd.DataFrame(data)
    
    print("Predicting...")
    pred = model.predict(df)
    print(f"Prediction: {pred}")

except Exception as e:
    print("CRITICAL ERROR IN PREDICTION:")
    traceback.print_exc()
