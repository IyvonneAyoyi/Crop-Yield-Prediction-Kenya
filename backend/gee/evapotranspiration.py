import ee

from .validation import validate_crop_county

from .helpers import (
    get_crop_mask,
    get_county,
    get_harvested_area
)

from .validation import validate_crop_county


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
