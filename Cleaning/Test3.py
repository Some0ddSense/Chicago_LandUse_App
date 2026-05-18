import geopandas as gpd
import pandas as pd

path = "CMAP_Area_Count/LUI_2020_Area.geojson"

gdf = gpd.read_file(path)

# List the land use columns you expect
land_use_columns = [
    'Single Family Residential', 'Multi-Family Residential', 'Commercial',
    'Urban Mix + Residential', 'Institutional', 'Industrial',
    'TCUW', 'Agricultural', 'Open Space', 'Vacant',
    'Under Construction', 'Water', 'Non-Parcel / Other', 'Total'
]

print("\n=== CHECK LAND USE COLUMNS EXIST ===")
for col in land_use_columns:
    print(col, "→", col in gdf.columns)

print("\n=== CHECK FIRST 5 VALUES OF SELECTED LAND USE ===")
col = "Multi-Family Residential"
print(gdf[col].head())

print("\n=== CHECK FIRST 5 VALUES OF TOTAL ===")
print(gdf["Total"].head())

print("\n=== COMPUTE PERCENT ===")
gdf["percent_land_use"] = (gdf[col] / gdf["Total"]) * 100
print(gdf["percent_land_use"].head())

