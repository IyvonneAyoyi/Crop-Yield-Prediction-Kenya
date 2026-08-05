import ee

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
