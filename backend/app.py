from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from predict import get_features
from model import predict_crop_yield

from gee.constants import (
    FEATURE_UNITS,
    SUPPORTED_CROPS,
    SUPPORTED_COUNTIES
)

# ==========================================================
# FASTAPI APP
# ==========================================================

app = FastAPI(
    title="Crop Yield Prediction API",
    description="Predict crop yield using Google Earth Engine and a trained Random Forest model.",
    version="1.0.0"
)

# ==========================================================
# ENABLE CORS
# ==========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # React (Vite)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================================
# DATE LIMITS
# ==========================================================

MIN_DATE = datetime(2000, 1, 1)
MAX_DATE = datetime.today()

# ==========================================================
# REQUEST MODEL
# ==========================================================

class PredictionRequest(BaseModel):
    crop: str
    county: str
    start_date: str
    end_date: str

# ==========================================================
# DATE VALIDATION
# ==========================================================

def validate_dates(start_date: str, end_date: str):

    try:

        start = datetime.strptime(
            start_date,
            "%Y-%m-%d"
        )

        end = datetime.strptime(
            end_date,
            "%Y-%m-%d"
        )

    except ValueError:

        raise HTTPException(
            status_code=400,
            detail="Dates must be in YYYY-MM-DD format."
        )

    if start >= end:

        raise HTTPException(
            status_code=400,
            detail="start_date must be earlier than end_date."
        )

    if start < MIN_DATE:

        raise HTTPException(
            status_code=400,
            detail="Satellite data is only available from 2000 onwards."
        )

    if end > MAX_DATE:

        raise HTTPException(
            status_code=400,
            detail="Future dates are not supported because satellite observations are not yet available."
        )

    return (
        start.strftime("%Y-%m-%d"),
        end.strftime("%Y-%m-%d")
    )

# ==========================================================
# HOME
# ==========================================================

@app.get("/")
def home():

    return {
        "message": "Crop Yield Prediction API is running."
    }

# ==========================================================
# AVAILABLE CROPS
# ==========================================================

@app.get("/crops")
def get_crops():

    return {
        "crops": SUPPORTED_CROPS
    }

# ==========================================================
# AVAILABLE COUNTIES
# ==========================================================

@app.get("/counties")
def get_counties():

    return {
        "counties": SUPPORTED_COUNTIES
    }

# ==========================================================
# PREDICT
# ==========================================================

@app.post("/predict")
def predict(request: PredictionRequest):

    try:

        # --------------------------------------------------
        # Validate crop
        # --------------------------------------------------

        if request.crop not in SUPPORTED_CROPS:

            raise HTTPException(
                status_code=400,
                detail=f"Unsupported crop '{request.crop}'."
            )

        # --------------------------------------------------
        # Validate county
        # --------------------------------------------------

        if request.county not in SUPPORTED_COUNTIES:

            raise HTTPException(
                status_code=400,
                detail=f"Unsupported county '{request.county}'."
            )

        # --------------------------------------------------
        # Validate dates
        # --------------------------------------------------

        start_date, end_date = validate_dates(
            request.start_date,
            request.end_date
        )

        # --------------------------------------------------
        # Step 1
        # Extract environmental variables
        # --------------------------------------------------

        features_df = get_features(
            crop_name=request.crop,
            county_name=request.county,
            start_date=start_date,
            end_date=end_date
        )

        feature_values = features_df.iloc[0].to_dict()

        environmental_variables = {}

        for feature, value in feature_values.items():

            environmental_variables[feature] = {
                "value": round(float(value), 3),
                "unit": FEATURE_UNITS.get(feature, "")
            }

        # --------------------------------------------------
        # Step 2
        # Predict yield
        # --------------------------------------------------

        predicted_yield = predict_crop_yield(
            features_df=features_df,
            crop_name=request.crop,
            county_name=request.county
        )

        # --------------------------------------------------
        # Step 3
        # Return response
        # --------------------------------------------------

        return {

            "model": {
                "name": "Random Forest Regressor",
                "version": "1.0"
            },

            "crop": request.crop,

            "county": request.county,

            "start_date": start_date,

            "end_date": end_date,

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
            status_code=500,
            detail=str(e)
        )