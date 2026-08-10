from backend.gee.rainfall import get_rainfall
from backend.gee.ndvi import get_ndvi
from backend.gee.lst import get_lst
from backend.gee.soil_moisture import get_soil_moisture
from backend.gee.evapotranspiration import get_evapotranspiration
from backend.gee.elevation import get_elevation
from backend.gee.slope import get_slope


def main():
    county = "Nakuru"
    crop = "Irish Potatoes"
    start = "2019-01-01"
    end = "2020-01-01"

    rainfall = get_rainfall(
        county_name=county,
        crop_name=crop,
        start_date=start,
        end_date=end
    )
    print(f"Weighted Rainfall: {rainfall:.3f} mm")

    ndvi = get_ndvi(
        county_name=county,
        crop_name=crop,
        start_date=start,
        end_date=end
    )
    print(f"Weighted NDVI: {ndvi:.6f}")

    lst = get_lst(
        county_name=county,
        crop_name=crop,
        start_date=start,
        end_date=end
    )
    print(f"LST: {lst:.3f} °C")

    soil = get_soil_moisture(
        county_name=county,
        crop_name=crop,
        start_date=start,
        end_date=end
    )
    print(f"Weighted Soil Moisture: {soil:.3f} m³/m³")

    et = get_evapotranspiration(
        county_name=county,
        crop_name=crop,
        start_date=start,
        end_date=end
    )
    print(f"Weighted ET: {et:.3f} mm")

    elevation = get_elevation(
        county_name=county,
        crop_name=crop
    )
    print(f"Weighted Elevation: {elevation:.3f} m")

    slope = get_slope(
        county_name=county,
        crop_name=crop
    )
    print(f"Weighted Slope: {slope:.3f} degrees")


if __name__ == "__main__":
    main()