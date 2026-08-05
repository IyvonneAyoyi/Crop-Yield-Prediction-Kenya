import ee

from .validation import validate_crop_county

from .helpers import (
    get_crop_mask,
    get_county,
    get_harvested_area
)

from .validation import validate_crop_county

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
