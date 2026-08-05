import ee

from gee.validation import validate_crop_county

from gee.rainfall import get_rainfall
from gee.ndvi import get_ndvi
from gee.lst import get_lst
from gee.soil_moisture import get_soil_moisture
from gee.evapotranspiration import get_evapotranspiration
from gee.elevation import get_elevation
from gee.slope import get_slope



from gee.config import (
    COUNTIES,
    CROP_MASKS
)

from gee.helpers import (
    get_crop_mask,
    get_county,
    get_harvested_area
)


    
# ==========================================================
# TESTING
# ==========================================================

if __name__ == "__main__":

    rainfall = get_rainfall(

        county_name="Nakuru",

        crop_name="Irish Potatoes",

        start_date="2019-01-01",

        end_date="2020-01-01"

    )

    print(f"Weighted Rainfall: {rainfall:.3f} mm")

    # NDVI TEST

    ndvi = get_ndvi(

        county_name="Nakuru",

        crop_name="Irish Potatoes",

        start_date="2019-01-01",

        end_date="2020-01-01"

    )

    print(f"Weighted NDVI: {ndvi:.6f}")

    # LST TEST

    lst = get_lst(

        county_name="Nakuru",

        crop_name="Irish Potatoes",

        start_date="2019-01-01",

        end_date="2020-01-01"

    )

    print(f"LST: {lst:.3f} °C")

    # Soil Moisture Test
    soil_moisture = get_soil_moisture(

        county_name="Nakuru",

        crop_name="Irish Potatoes",

        start_date="2019-01-01",

        end_date="2020-01-01"

    )

    print(f"Weighted Soil Moisture: {soil_moisture:.3f} m³/m³")

    # Evapotranspiration Test

et = get_evapotranspiration(

    county_name="Nakuru",

    crop_name="Irish Potatoes",

    start_date="2019-01-01",

    end_date="2020-01-01"

)

print(f"Weighted ET: {et:.3f} mm")

# Elevation Test

elevation = get_elevation(

    county_name="Nakuru",

    crop_name="Irish Potatoes"

)

print(f"Weighted Elevation: {elevation:.3f} m")

# Slope Test

slope = get_slope(

    county_name="Nakuru",

    crop_name="Irish Potatoes"

)

print(f"Weighted Slope: {slope:.3f} degrees")
