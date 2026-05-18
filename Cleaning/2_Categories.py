import geopandas as gpd
import pandas as pd
from glob import glob

def safe_sum(gdf, columns):
    """Sum only columns that exist in the GeoDataFrame"""
    existing_cols = [col for col in columns if col in gdf.columns]
    if not existing_cols:
        return 0
    return gdf[existing_cols].sum(axis=1)

for file_path in glob('CMAP_Area_Count/*.geojson'):
    print(f"\n--- Processing {file_path} ---")
    gdf = gpd.read_file(file_path)

    # ---------------------------------------------------------
    # STEP 1 — CLEAN LANDUSE COLUMNS (convert nulls + strings)
    # ---------------------------------------------------------
    landuse_cols = [c for c in gdf.columns if c.startswith("LANDUSE")]

    print("Columns being summed for TOTAL:")
    for col in landuse_cols:
        print("  -", col)

    # Convert to numeric and replace nulls with 0
    gdf[landuse_cols] = (
        gdf[landuse_cols]
        .apply(pd.to_numeric, errors='coerce')
        .fillna(0)
    )

    # ---------------------------------------------------------
    # STEP 2 — TOTAL BEFORE CATEGORY COLUMNS
    # ---------------------------------------------------------
    gdf['Total'] = gdf[landuse_cols].sum(axis=1)

    # ---------------------------------------------------------
    # STEP 3 — CATEGORY COLUMNS
    # ---------------------------------------------------------
    gdf['Single Family Residential'] = safe_sum(gdf, ['LANDUSE1110', 'LANDUSE1111', 'LANDUSE1112', 'LANDUSE1120', 'LANDUSE1140'])
    gdf['Multi-Family Residential'] = safe_sum(gdf, ['LANDUSE1130'])
    gdf['Commercial'] = safe_sum(gdf, [
        'LANDUSE1210', 'LANDUSE1211', 'LANDUSE1212', 'LANDUSE1214', 'LANDUSE1215',
        'LANDUSE1220', 'LANDUSE1221', 'LANDUSE1222', 'LANDUSE1223', 'LANDUSE1224',
        'LANDUSE1230', 'LANDUSE1231', 'LANDUSE1232', 'LANDUSE1240', 'LANDUSE1241',
        'LANDUSE1242', 'LANDUSE1243', 'LANDUSE1250', 'LANDUSE1260'
    ])
    gdf['Urban Mix + Residential'] = safe_sum(gdf, ['LANDUSE1216'])
    gdf['Institutional'] = safe_sum(gdf, [
        'LANDUSE1310', 'LANDUSE1311', 'LANDUSE1312', 'LANDUSE1313', 'LANDUSE1320',
        'LANDUSE1321', 'LANDUSE1322', 'LANDUSE1330', 'LANDUSE1340', 'LANDUSE1350',
        'LANDUSE1360', 'LANDUSE1370', 'LANDUSE1380', 'LANDUSE1390'
    ])
    gdf['Industrial'] = safe_sum(gdf, [
        'LANDUSE1410', 'LANDUSE1420', 'LANDUSE1430', 'LANDUSE1431', 'LANDUSE1432',
        'LANDUSE1433', 'LANDUSE1440', 'LANDUSE1450'
    ])
    gdf['TCUW'] = safe_sum(gdf, [
        'LANDUSE1510', 'LANDUSE1511', 'LANDUSE1512', 'LANDUSE1520', 'LANDUSE1530',
        'LANDUSE1540', 'LANDUSE1550', 'LANDUSE1560', 'LANDUSE1561', 'LANDUSE1562',
        'LANDUSE1563', 'LANDUSE1564', 'LANDUSE1565', 'LANDUSE1570'
    ])
    gdf['Agricultural'] = safe_sum(gdf, ['LANDUSE2000', 'LANDUSE2100', 'LANDUSE2200'])
    gdf['Open Space'] = safe_sum(gdf, [
        'LANDUSE1151', 'LANDUSE3100', 'LANDUSE3110', 'LANDUSE3120', 'LANDUSE3130',
        'LANDUSE3200', 'LANDUSE3210', 'LANDUSE3220', 'LANDUSE3300', 'LANDUSE3400',
        'LANDUSE3500', 'LANDUSE6100'
    ])
    gdf['Vacant'] = safe_sum(gdf, ['LANDUSE4110', 'LANDUSE4120', 'LANDUSE4130', 'LANDUSE4140', 'LANDUSE4300'])
    gdf['Under Construction'] = safe_sum(gdf, ['LANDUSE4210', 'LANDUSE4220', 'LANDUSE4230', 'LANDUSE4240'])
    gdf['Water'] = safe_sum(gdf, ['LANDUSE5000', 'LANDUSE5100', 'LANDUSE5200', 'LANDUSE5300', 'LANDUSE6200'])
    gdf['Non-Parcel / Other'] = safe_sum(gdf, ['LANDUSE6000', 'LANDUSE6300', 'LANDUSE6400', 'LANDUSE9999'])

    # ---------------------------------------------------------
    # STEP 4 — SAVE FILE
    # ---------------------------------------------------------
    gdf.to_file(file_path, driver='GeoJSON')
    print(f"✓ Updated {file_path}")

print("\nDone! TOTAL column added correctly and nulls fixed.")

