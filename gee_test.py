import ee

# Initialize Earth Engine
ee.Initialize(project="geospatial-rs")

print("✅ Google Earth Engine connected successfully!")

# Test using a public dataset
image = ee.Image("USGS/SRTMGL1_003")

print("Dataset:", image.get("system:id").getInfo())