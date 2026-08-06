import pandas as pd

from gee.rainfall import get_rainfall
from gee.ndvi import get_ndvi
from gee.lst import get_lst
from gee.soil_moisture import get_soil_moisture
from gee.evapotranspiration import get_evapotranspiration
from gee.elevation import get_elevation
from gee.slope import get_slope


from gee.constants import FEATURE_UNITS

def get_features(
    crop_name,
    county_name,
    start_date,
    end_date
):

    features = {
        "Rainfall": get_rainfall(
            county_name,
            crop_name,
            start_date,
            end_date
        ),

        "NDVI": get_ndvi(
            county_name,
            crop_name,
            start_date,
            end_date
        ),

        "Temperature": get_lst(
            county_name,
            crop_name,
            start_date,
            end_date
        ),

        "Soil_Moisture": get_soil_moisture(
            county_name,
            crop_name,
            start_date,
            end_date
        ),

        "Evapotranspiration": get_evapotranspiration(
            county_name,
            crop_name,
            start_date,
            end_date
        ),

        "Elevation": get_elevation(
            county_name,
            crop_name
        ),

        "Slope": get_slope(
            county_name,
            crop_name
        )
    }

    return pd.DataFrame([features])


# ==========================================================
# TESTING
# ==========================================================

if __name__ == "__main__":

    features = get_features(

        crop_name="Irish Potatoes",

        county_name="Nakuru",

        start_date="2019-01-01",

        end_date="2020-01-01"

    )

    print(features)