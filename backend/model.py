import joblib
from pathlib import Path

from .preprocessing import preprocess


# ==========================================================
# MODELS DIRECTORY
# ==========================================================

MODELS_DIR = (
    Path(__file__).resolve().parent
    /"app"
    / "models"
)


# ==========================================================
# LOAD MODEL
# ==========================================================

model = joblib.load(
    MODELS_DIR / "random_forest_model.pkl"
)


# ==========================================================
# PREDICT YIELD
# ==========================================================

def predict_crop_yield(
    features_df,
    crop_name,
    county_name
):
    """
    Predict crop yield from extracted
    environmental variables.
    """

    processed_features = preprocess(
        features_df,
        crop_name=crop_name,
        county_name=county_name
    )

    prediction = model.predict(
        processed_features
    )

    return float(prediction[0])