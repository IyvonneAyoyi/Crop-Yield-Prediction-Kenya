import ee
import os
import json

# ==========================================================
# GOOGLE EARTH ENGINE AUTHENTICATION
# ==========================================================

service_account = os.environ.get(
    "EARTH_ENGINE_SERVICE_ACCOUNT"
)

private_key = os.environ.get(
    "EARTH_ENGINE_PRIVATE_KEY"
)

if service_account and private_key:

    # Render / production

    private_key = private_key.replace("\\n", "\n")

    service_account_info = {
        "type": "service_account",
        "client_email": service_account,
        "private_key": private_key,
        "token_uri": "https://oauth2.googleapis.com/token"
    }

    credentials = ee.ServiceAccountCredentials(
        service_account,
        key_data=json.dumps(service_account_info)
    )

    ee.Initialize(
        credentials=credentials,
        project="geospatial-rs"
    )

else:

    # Local development

    ee.Initialize(
        project="geospatial-rs"
    )


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