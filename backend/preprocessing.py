import joblib
import pandas as pd
from pathlib import Path

from gee.constants import COUNTY_NAME_MAPPING

# ==========================================================
# MODELS DIRECTORY
# ==========================================================

MODELS_DIR = (
    Path(__file__).resolve().parent.parent
    / "models"
)

# ==========================================================
# LOAD TRAINED ENCODER
# ==========================================================

encoder = joblib.load(
    MODELS_DIR / "onehot_encoder.pkl"
)

# ==========================================================
# NUMERIC FEATURES (must match training)
# ==========================================================

numeric_columns = [
    "NDVI",
    "Rainfall_mm",
    "Temperature_C",
    "Elevation_m",
    "Slope_Degrees",
    "Soil_Moisture",
    "Evapotranspiration_mm"
]

# ==========================================================
# COMPLETE TRAINING COLUMN ORDER
# ==========================================================

training_columns = (
    numeric_columns +
    encoder.get_feature_names_out(
        ["County", "Crop"]
    ).tolist()
)

# ==========================================================
# PREPROCESS FEATURES
# ==========================================================

def preprocess(
    features_df,
    crop_name,
    county_name
):
    """
    Convert live GEE features into the exact
    feature format expected by the trained model.
    """

    # ------------------------------------------
    # Work on a copy
    # ------------------------------------------

    df = features_df.copy()

    # ------------------------------------------
    # Rename columns to training names
    # ------------------------------------------

    df = df.rename(columns={

        "Rainfall": "Rainfall_mm",

        "Temperature": "Temperature_C",

        "Elevation": "Elevation_m",

        "Slope": "Slope_Degrees",

        "Evapotranspiration": "Evapotranspiration_mm"

    })

    # ------------------------------------------
    # Match county names used during training
    # ------------------------------------------

    county_name = COUNTY_NAME_MAPPING.get(
        county_name,
        county_name
    )

    # ------------------------------------------
    # Add categorical columns
    # ------------------------------------------

    df["County"] = county_name

    df["Crop"] = crop_name

    # ------------------------------------------
    # One-Hot Encode County and Crop
    # ------------------------------------------

    encoded = encoder.transform(
        df[["County", "Crop"]]
    )

    encoded_df = pd.DataFrame(
        encoded,
        columns=encoder.get_feature_names_out(
            ["County", "Crop"]
        ),
        index=df.index
    )

    # ------------------------------------------
    # Remove original categorical columns
    # ------------------------------------------

    df = df.drop(
        columns=[
            "County",
            "Crop"
        ]
    )

    # ------------------------------------------
    # Append encoded columns
    # ------------------------------------------

    df = pd.concat(
        [
            df,
            encoded_df
        ],
        axis=1
    )

    # ------------------------------------------
    # Match exact training feature order
    # ------------------------------------------

    df = df.reindex(
        columns=training_columns,
        fill_value=0
    )

    return df


# ==========================================================
# TESTING
# ==========================================================

if __name__ == "__main__":

    from predict import get_features

    features = get_features(

        crop_name="Irish Potatoes",

        county_name="Nakuru",

        start_date="2019-01-01",

        end_date="2020-01-01"

    )

    processed = preprocess(

        features,

        crop_name="Irish Potatoes",

        county_name="Nakuru"

    )

    print(processed)

    print("\nShape:", processed.shape)

    print("\nColumns:")

    print(processed.columns.tolist())