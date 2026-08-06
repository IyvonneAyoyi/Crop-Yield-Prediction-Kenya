import joblib
from pathlib import Path

from predict import get_features
from preprocessing import preprocess


# ==========================================================
# MODELS DIRECTORY
# ==========================================================

MODELS_DIR = (
    Path(__file__).resolve().parent.parent
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

def predict_yield(processed_features):
    """
    Predict crop yield (t/ha)
    using the trained Random Forest model.
    """

    prediction = model.predict(
    processed_features
)

    return float(prediction[0])


# ==========================================================
# COMPLETE PREDICTION PIPELINE
# ==========================================================

def predict_crop_yield(
    crop_name,
    county_name,
    start_date,
    end_date
):
    """
    Complete prediction pipeline.

    1. Extract live GEE features.
    2. Preprocess them exactly as training.
    3. Predict yield.
    """

    # Step 1
    features = get_features(
        crop_name=crop_name,
        county_name=county_name,
        start_date=start_date,
        end_date=end_date
    )

    # Step 2
    processed_features = preprocess(
        features,
        crop_name=crop_name,
        county_name=county_name
    )

    # Step 3
    prediction = predict_yield(
        processed_features
    )

    return prediction


