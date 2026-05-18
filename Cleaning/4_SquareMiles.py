import geopandas as gpd
from pathlib import Path
import os

land_use_columns = [
    'Single Family Residential', 'Multi-Family Residential', 'Commercial',
    'Urban Mix + Residential', 'Institutional', 'Industrial',
    'TCUW', 'Agricultural', 'Open Space', 'Vacant',
    'Under Construction', 'Water', 'Non-Parcel / Other', 'Total'
]

SQFT_TO_SQMI = 1 / 27878400  # conversion factor

# Get directory and find all *Area.geojson files
data_dir = Path('CMAP_Area_Count')
area_files = sorted(data_dir.glob('*Area.geojson'))

if not area_files:
    print("No *Area.geojson files found in CMAP_Area_Count directory")
else:
    for file_path in area_files:
        print(f"Processing {file_path.name}...")
        gdf = gpd.read_file(file_path)
        
        # Convert land use columns from square feet to square miles
        for col in land_use_columns:
            if col in gdf.columns:
                gdf[col] = gdf[col] * SQFT_TO_SQMI
        
        # Save back to the same file
        gdf.to_file(file_path, driver='GeoJSON')
        print(f"✓ Updated {file_path.name}")

print("\nDone! All *Area.geojson files converted to square miles.")