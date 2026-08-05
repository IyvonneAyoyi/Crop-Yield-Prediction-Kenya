import ee

from .validation import validate_crop_county

from .helpers import (
    get_crop_mask,
    get_county,
    get_harvested_area
)

from .validation import validate_crop_county

# ==========================================================
# RAINFALL (CHIRPS)
# ==========================================================

def get_rainfall(
        county_name,
        crop_name,
        start_date,
        end_date
):
    """
    Calculate harvested-area weighted
    average rainfall.
    """

    # ----------------------------------
    # Validate user inputs
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
        scale=250
   )

    # ----------------------------------
    # CHIRPS rainfall
    # ----------------------------------

    rainfall = (
        ee.ImageCollection(
            "UCSB-CHG/CHIRPS/DAILY"
        )
        .select("precipitation")
        .filterDate(
            start_date,
            end_date
        )
        .sum()
    )

    # ----------------------------------
    # Weighted rainfall
    # ----------------------------------

    weighted_rainfall = rainfall.multiply(
        crop_mask
    )

    weighted_sum = weighted_rainfall.reduceRegion(

        reducer=ee.Reducer.sum(),

        geometry=county.geometry(),

        scale=250,

        maxPixels=1e13,

        bestEffort=True

    )

    rainfall_band = rainfall.bandNames().get(0)

    rainfall_total = ee.Number(
        weighted_sum.get(
            rainfall_band
        )
    )

    # ----------------------------------
    # Weighted mean rainfall
    # ----------------------------------

    rainfall_value = ee.Algorithms.If(

        harvested.gt(0),

        rainfall_total.divide(
            harvested
        ),

        None

    )

    return ee.Number(
        rainfall_value
    ).getInfo()


