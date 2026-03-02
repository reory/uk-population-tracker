import os
import geopandas as gpd
import pytest

# This test ensures that the critical uk_regions.gpkg file exists and is readable. 
# If this fails, the maps won't render.

def test_geo_package_exists():
    """Check if the ONS boundary data is in the correct path."""

    path = os.path.join("data", "geography", "uk_regions.gpkg")
    assert os.path.exists(path), f"CRITICAL: GeoPackage missing at {path}"

def test_geo_package_readable():
    """Check if GeoPandas can actually open the file and find the regions."""

    path = os.path.join("data", "geography", "uk_regions.gpkg")
    gdf = gpd.read_file(path)
    assert not gdf.empty

    # Adjust name if GPKG column header for region is different.
    expected_columns = ["name", "REGION", "nuts118nm"]
    assert any(col in gdf.columns for col in expected_columns)