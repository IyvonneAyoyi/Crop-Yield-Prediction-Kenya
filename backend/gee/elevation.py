import ee

from .validation import validate_crop_county

from .helpers import (
    get_crop_mask,
    get_county,
    get_harvested_area
)

from .validation import validate_crop_county

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
