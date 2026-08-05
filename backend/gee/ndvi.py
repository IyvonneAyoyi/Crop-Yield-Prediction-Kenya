import ee

from .validation import validate_crop_county

from .helpers import (
    get_crop_mask,
    get_county,
    get_harvested_area
)

from .validation import validate_crop_county


# ==========================================================
# NDVI (MODIS MOD13Q1)
# ==========================================================

def get_ndvi(
        county_name,
        crop_name,
        start_date,
        end_date
):
    """
    Calculate harvested-area weighted
    average NDVI.
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
    # MODIS NDVI
    # ----------------------------------

    ndvi = (
        ee.ImageCollection(
            "MODIS/061/MOD13Q1"
        )
        .select("NDVI")
        .filterDate(
            start_date,
            end_date
        )
        .mean()
        .multiply(0.0001)
    )

    # ----------------------------------
    # Weighted NDVI
    # ----------------------------------

    weighted_ndvi = ndvi.multiply(
        crop_mask
    )

    weighted_sum = weighted_ndvi.reduceRegion(

        reducer=ee.Reducer.sum(),

        geometry=county.geometry(),

        scale=250,

        maxPixels=1e13,

        bestEffort=True

    )

    ndvi_band = ndvi.bandNames().get(0)

    ndvi_total = ee.Number(
        weighted_sum.get(
            ndvi_band
        )
    )

    # ----------------------------------
    # Weighted mean NDVI
    # ----------------------------------

    ndvi_value = ee.Algorithms.If(

        harvested.gt(0),

        ndvi_total.divide(
            harvested
        ),

        None

    )

    return ee.Number(
        ndvi_value
    ).getInfo()
