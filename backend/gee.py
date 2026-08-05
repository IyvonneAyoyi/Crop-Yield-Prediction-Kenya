import ee
import pandas as pd
from pathlib import Path

# ==========================================================
# INITIALIZE EARTH ENGINE
# ==========================================================

ee.Initialize(project="geospatial-rs")

# ==========================================================
# LOAD COUNTY BOUNDARIES
# ==========================================================

COUNTIES = ee.FeatureCollection(
    "projects/geospatial-rs/assets/Kenya_Counties_Shapefiles"
)

# ==========================================================
# SPAM CROP MASKS
# ==========================================================

CROP_MASKS = {

    "Maize":
    "projects/geospatial-rs/assets/spam2020_V2r2_global_H_MAIZE",

    "Beans":
    "projects/geospatial-rs/assets/spam2020_V2r2_global_H_BEANS",

    "Cowpeas":
    "projects/geospatial-rs/assets/spam2020_V2r2_global_H_COWPEAS",

    "Irish Potatoes":
    "projects/geospatial-rs/assets/spam2020_V2r2_global_H_IRISHPOTATOES",

    "Pigeon Peas":
    "projects/geospatial-rs/assets/spam2020_V2r2_global_H_PIGEONPEAS",

    "Sorghum":
    "projects/geospatial-rs/assets/spam2020_V2r2_global_H_SORGHUM",

    "Sweet Potatoes":
    "projects/geospatial-rs/assets/spam2020_V2r2_global_H_SWEETPOTATOES",

    "Wheat":
    "projects/geospatial-rs/assets/spam2020_V2r2_global_H_WHEAT"

}

# ==========================================================
# VALID COUNTY-CROP COMBINATIONS
# ==========================================================

csv_path = (
    Path(__file__).resolve().parent
    / "data"
    / "valid_counties.csv"
)

valid_df = pd.read_csv(csv_path)

VALID_COUNTIES = (
    valid_df
    .groupby("Crop")["County"]
    .apply(list)
    .to_dict()
)

# ==========================================================
# VALIDATION
# ==========================================================

def validate_crop_county(crop_name, county_name):
    """
    Ensure the selected crop-county combination
    exists in the training dataset.
    """

    # Check supported crop
    if crop_name not in CROP_MASKS:
        raise ValueError(
            f"Crop '{crop_name}' is not supported."
        )

    # Check crop exists in training data
    if crop_name not in VALID_COUNTIES.keys():
        raise ValueError(
            f"No counties found for crop '{crop_name}'."
        )

    # Check valid crop-county combination
    if county_name not in VALID_COUNTIES[crop_name]:
        raise ValueError(
            f"{crop_name} was not included for "
            f"{county_name} during model training."
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

def get_harvested_area(crop_mask, county):
    """
    Calculate harvested area
    inside the selected county.
    """

    band_name = crop_mask.bandNames().get(0)

    harvested_area = crop_mask.reduceRegion(

        reducer=ee.Reducer.sum(),

        geometry=county.geometry(),

        scale=250,

        maxPixels=1e13,

        bestEffort=True

    )

    return ee.Number(
        harvested_area.get(band_name)
    )


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
        county
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