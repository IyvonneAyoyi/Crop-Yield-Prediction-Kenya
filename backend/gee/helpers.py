import ee

from .config import (
    COUNTIES,
    CROP_MASKS
)


# ==========================================================
# LOAD CROP MASK
# ==========================================================

def get_crop_mask(crop_name):
    """
    Load the SPAM harvested area raster
    for the selected crop.
    """

    asset_id = CROP_MASKS[crop_name]

    return ee.Image(asset_id)


# ==========================================================
# LOAD COUNTY
# ==========================================================

def get_county(county_name):
    """
    Retrieve the selected county boundary.
    """

    county = (
        COUNTIES
        .filter(
            ee.Filter.eq(
                "ADM1_EN",
                county_name
            )
        )
        .first()
    )

    if county.getInfo() is None:
        raise ValueError(
            f"County '{county_name}' not found."
        )

    return county


# ==========================================================
# HARVESTED AREA
# ==========================================================

def get_harvested_area(crop_mask, county, scale):
    """
    Calculate harvested area inside the selected county.
    """

    band_name = crop_mask.bandNames().get(0)

    harvested_area = crop_mask.reduceRegion(
        reducer=ee.Reducer.sum(),
        geometry=county.geometry(),
        scale=scale,
        maxPixels=1e13,
        bestEffort=True
    )

    return ee.Number(
        harvested_area.get(band_name)
    )
