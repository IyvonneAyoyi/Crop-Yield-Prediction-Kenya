import pandas as pd
from pathlib import Path

from .config import CROP_MASKS



# ==========================================================
# VALID COUNTY-CROP COMBINATIONS
# ==========================================================

csv_path = (
    Path(__file__).resolve().parent.parent
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