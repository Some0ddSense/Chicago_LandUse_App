import geopandas as gpd
import json

path = "CMAP_Area_Count/LUI_1990_Count.geojson"  # change year if needed

# Load GDF
gdf = gpd.read_file(path)

print("\nGDF COLUMNS:")
print(gdf.columns.tolist())

# Load raw JSON
with open(path, "r") as f:
    raw = json.load(f)

print("\nRAW JSON PROPERTIES:")
print(list(raw["features"][0]["properties"].keys()))

# Load JSON produced by gdf.to_json()
raw_from_gdf = json.loads(gdf.to_json())

print("\nPROPERTIES IN gdf.to_json():")
print(list(raw_from_gdf["features"][0]["properties"].keys()))
