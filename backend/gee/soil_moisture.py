import ee

from .validation import validate_crop_county

from .helpers import (
    get_crop_mask,
    get_county,
    get_harvested_area
)

from .validation import validate_crop_county


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