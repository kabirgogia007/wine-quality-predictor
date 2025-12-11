# Wine Quality - RandomizedSearchCV (fast + high-quality)
# Assumes you have ucimlrepo installed and sklearn recent enough to include HistGradientBoostingRegressor.

from ucimlrepo import fetch_ucirepo
import pandas as pd
import numpy as np
import time
import joblib

from scipy.stats import randint, uniform
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, make_scorer

# Choose default estimator: "hist" or "gbrt"
# hist = faster (recommended). gbrt = sklearn.ensemble.GradientBoostingRegressor (slower)
USE_HIST = True

if USE_HIST:
    from sklearn.ensemble import HistGradientBoostingRegressor as EstimatorClass
else:
    from sklearn.ensemble import GradientBoostingRegressor as EstimatorClass

# ---------------------
# 1) Load dataset
# ---------------------
print("Loading dataset from UCI repository (id=186)...")
wine_quality = fetch_ucirepo(id=186)

# fetch_ucirepo returns structures with .data.features and .data.targets typically as pandas DataFrames/Series
X = wine_quality.data.features
y = wine_quality.data.targets

# Ensure correct types
if not isinstance(X, pd.DataFrame):
    X = pd.DataFrame(X)
if hasattr(y, "values"):
    y = y.values
y = np.ravel(y)   # flatten to 1D if necessary

print("X shape:", X.shape, "y shape:", y.shape)
print("Unique target values (example):", np.unique(y)[:10])

# ---------------------
# 2) Train/test split
# ---------------------
# Create stratification bins: Low (3-5), Mid (6), High (7+)
# np.digitize with bins=[6, 7] maps: <6 -> 0, 6 -> 1, >=7 -> 2
bins = np.digitize(y, bins=[6, 7])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=bins
)
print("Train shape:", X_train.shape, "Test shape:", X_test.shape)

# ---------------------
# 3) Pipeline + estimator
# ---------------------
# Note: HistGradientBoostingRegressor often performs better/faster on tabular data and has built-in early stopping.
# If you use Hist, scaling is typically unnecessary; we omit scaler to keep it faster.
if USE_HIST:
    # use the faster pipeline (no scaler)
    pipeline = Pipeline([
        ("model", EstimatorClass(random_state=42, early_stopping=True))
    ])
else:
    # if using GradientBoostingRegressor (classic), keep early stopping parameters and include a scaler
    from sklearn.preprocessing import RobustScaler
    pipeline = Pipeline([
        ("scaler", RobustScaler()),
        ("model", EstimatorClass(random_state=42, n_iter_no_change=10, validation_fraction=0.1, tol=1e-4))
    ])

# ---------------------
# 4) Parameter distributions (Randomized)
# ---------------------
if USE_HIST:
    # HistGradientBoosting parameter space
    param_distributions = {
        "model__max_iter": randint(200, 1200),
        "model__learning_rate": uniform(0.01, 0.2),
        "model__max_leaf_nodes": randint(16, 128),
        "model__min_samples_leaf": randint(1, 50),
        "model__max_depth": randint(3, 12),
        "model__l2_regularization": uniform(0.0, 1.0)
    }
else:
    # GradientBoostingRegressor param space
    param_distributions = {
        "model__n_estimators": randint(100, 800),
        "model__learning_rate": uniform(0.01, 0.29),
        "model__max_depth": randint(2, 9),
        "model__subsample": uniform(0.6, 0.4),
        "model__min_samples_split": randint(2, 11),
    }

# ---------------------
# 5) RandomizedSearchCV setup
# ---------------------

# Custom weighted MAE scorer (double penalty for high quality wines >= 7)
def weighted_mae(y_true, y_pred):
    errors = np.abs(y_true - y_pred)
    weights = np.where(y_true >= 7, 2.0, 1.0)
    return np.average(errors, weights=weights)

custom_scorer = make_scorer(weighted_mae, greater_is_better=False)

rnd = RandomizedSearchCV(
    estimator=pipeline,
    param_distributions=param_distributions,
    n_iter=30,                  # budget: 30 random combos (good default)
    scoring=custom_scorer,      # custom metric
    cv=4,                       # 4-fold CV for a balance of speed/robustness
    random_state=42,
    n_jobs=-1,                  # use all cores
    verbose=2,
    return_train_score=True,
    refit=True
)

# ---------------------
# 6) Fit
# ---------------------
print("Starting RandomizedSearchCV (this can take a few minutes depending on CPU)...")
t0 = time.time()
try:
    rnd.fit(X_train, y_train)
except Exception as e:
    print("ERROR during fit:", e)
    raise
elapsed = time.time() - t0
print(f"RandomizedSearchCV finished in {elapsed/60:.2f} minutes")

# ---------------------
# 7) Best results
# ---------------------
print("\n=== Best Cross-Validated Results ===")
print("Best CV R²:        ", rnd.best_score_)
print("Best parameters:   ", rnd.best_params_)

# ---------------------
# 8) Evaluate on test set
# ---------------------
best_model = rnd.best_estimator_
y_pred = best_model.predict(X_test)

rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\n=== Test set performance ===")
print("Test RMSE:  ", rmse)
print("Test MAE:   ", mae)
print("Test R²:    ", r2)

# ---------------------
# 9) Save best model
# ---------------------
OUTPATH = "best_model_wine_quality.joblib"
joblib.dump(best_model, OUTPATH)
print(f"\nSaved best model to: {OUTPATH}")

# ---------------------
# 9b) Save metadata (Features & Metrics)
# ---------------------
import json

# Save feature names
feature_names = list(X.columns)
with open("feature_names.json", "w") as f:
    json.dump(feature_names, f)
print("Saved feature_names.json")

# Save metrics
metrics = {
    "rmse": rmse,
    "mae": mae,
    "r2": r2
}
with open("metrics.json", "w") as f:
    json.dump(metrics, f)
print("Saved metrics.json")

# ---------------------
# 10) Quick CV summary: top 5 candidates
# ---------------------
import pandas as pd
cvres = pd.DataFrame(rnd.cv_results_)
summary_cols = ["rank_test_score", "mean_test_score", "std_test_score", "params"]
top5 = cvres[summary_cols].sort_values("rank_test_score").head(5)
pd.set_option("display.max_colwidth", 120)
print("\nTop 5 candidate results (CV):")
print(top5.to_string(index=False))
# ---------------------
