import ee

from .validation import validate_crop_county

from .helpers import (
    get_crop_mask,
    get_county,
    get_harvested_area
)

from .validation import validate_crop_county



# ==========================================================
# LAND SURFACE TEMPERATURE (MODIS)
# ==========================================================

def get_lst(
        county_name,
        crop_name,
        start_date,
        end_date
):
    """
    Calculate harvested-area weighted
    average Land Surface Temperature (°C).
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
         scale=1000
    )

    # ==========================================================
# LAND SURFACE TEMPERATURE (MODIS MOD11A2)
# ==========================================================

def get_lst(
        county_name,
        crop_name,
        start_date,
        end_date
):
    """
    Calculate harvested-area weighted
    average Land Surface Temperature (°C).
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
    # Crop raster
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
    # IMPORTANT: use 1000 m to match JS
    # ----------------------------------

    harvested = get_harvested_area(
        crop_mask,
        county,
        scale=1000
    )

    # ----------------------------------
    # MODIS LST
    # ----------------------------------

    lst = (
        ee.ImageCollection(
            "MODIS/061/MOD11A2"
        )
        .select("LST_Day_1km")
        .filterDate(
            start_date,
            end_date
        )
        .mean()
        .multiply(0.02)
        .subtract(273.15)
    )

    # ----------------------------------
    # Weighted temperature
    # ----------------------------------

    weighted_lst = lst.multiply(
        crop_mask
    )

    weighted_sum = weighted_lst.reduceRegion(

        reducer=ee.Reducer.sum(),

        geometry=county.geometry(),

        scale=1000,

        maxPixels=1e13,

        bestEffort=True

    )

    lst_band = lst.bandNames().get(0)

    lst_total = ee.Number(
        weighted_sum.get(
            lst_band
        )
    )

    # ----------------------------------
    # Weighted mean temperature
    # ----------------------------------

    lst_value = ee.Algorithms.If(

        harvested.gt(0),

        lst_total.divide(
            harvested
        ),

        None

    )

    return ee.Number(
        lst_value
    ).getInfo()