import ee

from gee.validation import validate_crop_county

from gee.rainfall import get_rainfall
from gee.ndvi import get_ndvi
from gee.lst import get_lst





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
# SOIL MOISTURE (ERA5-LAND)
# ==========================================================

def get_soil_moisture(
        county_name,
        crop_name,
        start_date,
        end_date
):
    """
    Calculate harvested-area weighted
    average soil moisture.
    """

    # ----------------------------------
    # Validate inputs
    # ----------------------------------

    validate_crop_county(
        crop_name,
        county_name
    )

    # ----------------------------------
    # County
    # ----------------------------------

    county = get_county(
        county_name
    )

    # ----------------------------------
    # Crop mask
    # ----------------------------------

    crop_raster = get_crop_mask(
        crop_name
    )

    crop_raster = crop_raster.clip(
        county.geometry()
    )

    crop_mask = crop_raster.updateMask(
        crop_raster.gt(0)
    )

    # ----------------------------------
    # Harvested area
    # ----------------------------------

    harvested = get_harvested_area(
        crop_mask,
        county,
        scale=9000
    )

    # ----------------------------------
    # ERA5-LAND Soil Moisture
    # ----------------------------------

    soil = (

        ee.ImageCollection(
            "ECMWF/ERA5_LAND/MONTHLY_AGGR"
        )

        .select(
            "volumetric_soil_water_layer_1"
        )

        .filterDate(
            start_date,
            end_date
        )

        .mean()

    )

    # ----------------------------------
    # Weighted Soil Moisture
    # ----------------------------------

    weighted_soil = soil.multiply(
        crop_mask
    )

    weighted_sum = weighted_soil.reduceRegion(

        reducer=ee.Reducer.sum(),

        geometry=county.geometry(),

        scale=9000,

        maxPixels=1e13,

        bestEffort=True

    )

    soil_band = soil.bandNames().get(0)

    soil_total = ee.Number(

        weighted_sum.get(
            soil_band
        )

    )

    # ----------------------------------
    # Weighted Mean Soil Moisture
    # ----------------------------------

    soil_value = ee.Algorithms.If(

        harvested.gt(0),

        soil_total.divide(
            harvested
        ),

        None

    )

    return ee.Number(
        soil_value
    ).getInfo()

# ==========================================================
# EVAPOTRANSPIRATION (MODIS MOD16A2GF)
# ==========================================================

def get_evapotranspiration(
        county_name,
        crop_name,
        start_date,
        end_date
):
    """
    Calculate harvested-area weighted
    average evapotranspiration (mm).
    """

    # ----------------------------------
    # Validate inputs
    # ----------------------------------

    validate_crop_county(
        crop_name,
        county_name
    )

    # ----------------------------------
    # County
    # ----------------------------------

    county = get_county(
        county_name
    )

    # ----------------------------------
    # Crop mask
    # ----------------------------------

    crop_raster = get_crop_mask(
        crop_name
    )

    crop_raster = crop_raster.clip(
        county.geometry()
    )

    crop_mask = crop_raster.updateMask(
        crop_raster.gt(0)
    )

    # ----------------------------------
    # Harvested area
    # ----------------------------------

    harvested = get_harvested_area(
        crop_mask,
        county,
        scale=500
    )

    # ----------------------------------
    # MODIS ET
    # ----------------------------------

    et = (

        ee.ImageCollection(
            "MODIS/061/MOD16A2GF"
        )

        .select("ET")

        .filterDate(
            start_date,
            end_date
        )

        .sum()

        .multiply(0.1)

    )

    # ----------------------------------
    # Weighted ET
    # ----------------------------------

    weighted_et = et.multiply(
        crop_mask
    )

    weighted_sum = weighted_et.reduceRegion(

        reducer=ee.Reducer.sum(),

        geometry=county.geometry(),

        scale=500,

        maxPixels=1e13,

        bestEffort=True

    )

    et_band = et.bandNames().get(0)

    et_total = ee.Number(

        weighted_sum.get(
            et_band
        )

    )

    # ----------------------------------
    # Weighted mean ET
    # ----------------------------------

    et_value = ee.Algorithms.If(

        harvested.gt(0),

        et_total.divide(
            harvested
        ),

        None

    )

    return ee.Number(
        et_value
    ).getInfo()

# ==========================================================
# ELEVATION (SRTM)
# ==========================================================

def get_elevation(
        county_name,
        crop_name
):
    """
    Calculate harvested-area weighted
    average elevation (m).
    """

    # ----------------------------------
    # Validate inputs
    # ----------------------------------

    validate_crop_county(
        crop_name,
        county_name
    )

    # ----------------------------------
    # County
    # ----------------------------------

    county = get_county(
        county_name
    )

    # ----------------------------------
    # Crop mask
    # ----------------------------------

    crop_raster = get_crop_mask(
        crop_name
    )

    crop_raster = crop_raster.clip(
        county.geometry()
    )

    crop_mask = crop_raster.updateMask(
        crop_raster.gt(0)
    )

    # ----------------------------------
    # Harvested area
    # ----------------------------------

    harvested = get_harvested_area(
        crop_mask,
        county,
        scale=30
    )

    # ----------------------------------
    # SRTM Elevation
    # ----------------------------------

    elevation = ee.Image(
        "USGS/SRTMGL1_003"
    )

    # ----------------------------------
    # Weighted Elevation
    # ----------------------------------

    weighted_elevation = elevation.multiply(
        crop_mask
    )

    weighted_sum = weighted_elevation.reduceRegion(

        reducer=ee.Reducer.sum(),

        geometry=county.geometry(),

        scale=30,

        maxPixels=1e13,

        bestEffort=True

    )

    elevation_total = ee.Number(
        weighted_sum.get("elevation")
    )

    # ----------------------------------
    # Weighted Mean Elevation
    # ----------------------------------

    elevation_value = ee.Algorithms.If(

        harvested.gt(0),

        elevation_total.divide(
            harvested
        ),

        None

    )

    return ee.Number(
        elevation_value
    ).getInfo()


# ==========================================================
# SLOPE (SRTM)
# ==========================================================

def get_slope(
        county_name,
        crop_name
):
    """
    Calculate harvested-area weighted
    average slope (degrees).
    """

    # ----------------------------------
    # Validate inputs
    # ----------------------------------

    validate_crop_county(
        crop_name,
        county_name
    )

    # ----------------------------------
    # County
    # ----------------------------------

    county = get_county(
        county_name
    )

    # ----------------------------------
    # Crop mask
    # ----------------------------------

    crop_raster = get_crop_mask(
        crop_name
    )

    crop_raster = crop_raster.clip(
        county.geometry()
    )

    crop_mask = crop_raster.updateMask(
        crop_raster.gt(0)
    )

    # ----------------------------------
    # Harvested area
    # ----------------------------------

    harvested = get_harvested_area(

        crop_mask,

        county,

        scale=30

    )

    # ----------------------------------
    # SRTM DEM
    # ----------------------------------

    dem = ee.Image(
        "USGS/SRTMGL1_003"
    )

    # ----------------------------------
    # Calculate slope
    # ----------------------------------

    slope = ee.Terrain.slope(
        dem
    )

    # ----------------------------------
    # Weighted slope
    # ----------------------------------

    weighted_slope = slope.multiply(
        crop_mask
    )

    weighted_sum = weighted_slope.reduceRegion(

        reducer=ee.Reducer.sum(),

        geometry=county.geometry(),

        scale=30,

        maxPixels=1e13,

        bestEffort=True

    )

    slope_band = slope.bandNames().get(0)

    slope_total = ee.Number(

        weighted_sum.get(
            slope_band
        )

    )

    # ----------------------------------
    # Weighted mean slope
    # ----------------------------------

    slope_value = ee.Algorithms.If(

        harvested.gt(0),

        slope_total.divide(
            harvested
        ),

        None

    )

    return ee.Number(
        slope_value
    ).getInfo()

    
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
