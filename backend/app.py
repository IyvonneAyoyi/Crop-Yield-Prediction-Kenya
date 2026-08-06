from datetime import date

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from predict import get_features
from model import predict_crop_yield
from gee.constants import FEATURE_UNITS


# ==========================================================
# FASTAPI APP
# ==========================================================

app = FastAPI(
    title="Crop Yield Prediction API",
    description="Predict crop yield using Google Earth Engine and a trained Random Forest model.",
    version="1.0.0"
)


# ==========================================================
# REQUEST MODEL
# ==========================================================

class PredictionRequest(BaseModel):
    crop: str
    county: str
    start_date: str
    end_date: str


# ==========================================================
# HOME
# ==========================================================

@app.get("/")
def home():
    return {
        "message": "Crop Yield Prediction API is running."
    }


# ==========================================================
# PREDICT
# ==========================================================

@app.post("/predict")
def predict(request: PredictionRequest):

    try:

        # -----------------------------------------
        # Validate dates
        # -----------------------------------------

        start = date.fromisoformat(request.start_date)
        end = date.fromisoformat(request.end_date)
        today = date.today()

        if end <= start:
            raise HTTPException(
                status_code=400,
                detail="End date must be after start date."
            )

        if start > today:
            raise HTTPException(
                status_code=400,
                detail="Future date ranges are not supported because satellite observations do not yet exist."
            )

        if end > today:
            end = today

        # -----------------------------------------
        # Step 1
        # Extract environmental variables
        # -----------------------------------------

        features_df = get_features(
            crop_name=request.crop,
            county_name=request.county,
            start_date=str(start),
            end_date=str(end)
        )

        feature_values = features_df.iloc[0].to_dict()

        environmental_variables = {}

        for feature, value in feature_values.items():

            environmental_variables[feature] = {
                "value": round(float(value), 3),
                "unit": FEATURE_UNITS.get(feature, "")
            }

        # -----------------------------------------
        # Step 2
        # Predict yield
        # -----------------------------------------

        predicted_yield = predict_crop_yield(
            features_df=features_df,
            crop_name=request.crop,
            county_name=request.county
        )

        # -----------------------------------------
        # Step 3
        # Response
        # -----------------------------------------

        return {

            "crop": request.crop,

            "county": request.county,

            "start_date": str(start),

            "end_date": str(end),

            "environmental_variables": environmental_variables,

            "predicted_yield": {
                "value": round(predicted_yield, 3),
                "unit": "t/ha"
            }

        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )