import streamlit as st
import geopandas as gpd
import pandas as pd
import folium
from streamlit_folium import st_folium

@st.cache_data
def load_geojson(path):
    gdf = gpd.read_file(path)
    gdf["community"] = gdf["community"].str.title()
    return gdf


# Available years
files = {
    "Parcel Area": {
        '1990': 'CMAP_Area_Count/LUI_1990_Area.geojson',
        '2001': 'CMAP_Area_Count/LUI_2001_Area.geojson',
        '2005': 'CMAP_Area_Count/LUI_2005_Area.geojson',
        '2010': 'CMAP_Area_Count/LUI_2010_Area.geojson',
        '2015': 'CMAP_Area_Count/LUI_2015_Area.geojson',
        '2020': 'CMAP_Area_Count/LUI_2020_Area.geojson',
        '2023': 'CMAP_Area_Count/LUI_2023_Area.geojson',
    },
    "Parcel Count": {
        '1990': 'CMAP_Area_Count/LUI_1990_Count.geojson',
        '2001': 'CMAP_Area_Count/LUI_2001_Count.geojson',
        '2005': 'CMAP_Area_Count/LUI_2005_Count.geojson',
        '2010': 'CMAP_Area_Count/LUI_2010_Count.geojson',
        '2015': 'CMAP_Area_Count/LUI_2015_Count.geojson',
        '2020': 'CMAP_Area_Count/LUI_2020_Count.geojson',
        '2023': 'CMAP_Area_Count/LUI_2023_Count.geojson',
    }
}

# Land use groups (exclude Total)
land_use_columns = [
    'Single Family Residential', 'Multi-Family Residential', 'Commercial',
    'Urban Mix + Residential', 'Institutional', 'Industrial',
    'TCUW', 'Agricultural', 'Open Space', 'Vacant',
    'Under Construction', 'Water', 'Non-Parcel / Other'
]


# Sidebar controls
st.sidebar.header("Change Map Controls")
selected_type = st.sidebar.selectbox("Select Data Type:", ["Parcel Area", "Parcel Count"])
if selected_type == "Parcel Area":
    selected_norm = st.sidebar.selectbox("Normalize By:", ["Square Miles", "Percentage"])
else:
    selected_norm = st.sidebar.selectbox("Normalize By:", ["Count", "Percentage"])
year_a = st.sidebar.selectbox("Select Start Year:", list(files[selected_type].keys()), index=0)
year_b = st.sidebar.selectbox("Select End Year:", list(files[selected_type].keys()), index=6)
selected_land_use = st.sidebar.selectbox("Select Land Use Category:", land_use_columns)

st.header(f"Land Use {selected_type} {selected_land_use} Change Analysis ({year_a} to {year_b})")

if year_a == year_b:
    st.warning("Please select two different years.")
    st.stop()

# Load both years
gdf_a = load_geojson(files[selected_type][year_a])
gdf_b = load_geojson(files[selected_type][year_b])

# Ensure numeric
for col in land_use_columns + ["Total"]:
    gdf_a[col] = pd.to_numeric(gdf_a[col], errors="coerce")
    gdf_b[col] = pd.to_numeric(gdf_b[col], errors="coerce") 
    
# Fix geometries
gdf_a["geometry"] = gdf_a["geometry"].buffer(0)
gdf_b["geometry"] = gdf_b["geometry"].buffer(0)

# Merge on community area ID
merged = gdf_a[["BoundsP_area_numbe", "community", selected_land_use, "Total", "geometry"]].merge(
    gdf_b[["BoundsP_area_numbe", selected_land_use, "Total"]],
    on="BoundsP_area_numbe",
    suffixes=("_A", "_B")
)

# Compute percent values for each year
merged["pct_A"] = (merged[f"{selected_land_use}_A"] / merged["Total_A"]) * 100
merged["pct_B"] = (merged[f"{selected_land_use}_B"] / merged["Total_B"]) * 100

# Compute percent change
merged["pct_change"] = ((merged["pct_B"] - merged["pct_A"]) / merged["pct_A"]) * 100
merged["pct_change"] = merged["pct_change"].replace([float("inf"), -float("inf")], 0).fillna(0)
merged["area_change"] = ((merged[f"{selected_land_use}_B"] - merged[f"{selected_land_use}_A"]) / merged[f"{selected_land_use}_A"]) * 100
merged["area_change"] = merged["area_change"].replace([float("inf"), -float("inf")], 0).fillna(0)

# -------------------------
# FORMAT VALUES WITH + SIGN
# -------------------------
if selected_norm == "Percentage":
    merged["pct_A_fmt"] = merged["pct_A"].apply(lambda x: f"{x:.1f}%")
    merged["pct_B_fmt"] = merged["pct_B"].apply(lambda x: f"{x:.1f}%")
    merged["pct_change_fmt"] = merged["pct_change"].apply(
        lambda x: f"+{x:.1f}%" if x > 0 else f"{x:.1f}%"
    )
else:
    merged["area_change_fmt"] = merged["area_change"].apply(
        lambda x: f"+{x:.2f}" if x > 0 else f"{x:.2f}"
    )

# Force symmetric color scale around 0
if selected_norm == "Percentage":
    max_abs = merged["pct_change"].abs().max()
    vmin, vmax = -max_abs, max_abs
elif selected_norm == "Square Miles":
    max_abs = merged["area_change"].abs().max()
    vmin, vmax = -max_abs, max_abs

# Map center
center_lat = merged.geometry.centroid.y.mean()
center_lon = merged.geometry.centroid.x.mean()

# Create map
m = folium.Map(location=[center_lat, center_lon], zoom_start=10, min_zoom=9,tiles="Cartodb.voyagernolabels")

# Diverging choropleth with 0 as critical break
if selected_norm == "Percentage":
    folium.Choropleth(
        geo_data=merged.to_json(),
        data=merged,
        columns=["BoundsP_area_numbe", "pct_change"],
        key_on="properties.BoundsP_area_numbe",
        fill_color="RdYlBu",
        fill_opacity=0.8,
        line_opacity=0.2,
        nan_fill_color="white",
        legend_name=f"% Change in {selected_land_use} ({year_a} → {year_b})",
        threshold_scale=[vmin, vmin*0.75, vmin*0.5, vmin*0.25, 0, vmax*0.25, vmax*0.5, vmax*0.75, vmax]
    ).add_to(m)
elif selected_norm == "Square Miles":
    folium.Choropleth(
        geo_data=merged.to_json(),
        data=merged,
        columns=["BoundsP_area_numbe", "area_change"],
        key_on="properties.BoundsP_area_numbe",
        fill_color="RdYlBu",
        fill_opacity=0.8,
        line_opacity=0.2,
        nan_fill_color="white",
        legend_name=f"% Change in {selected_land_use} ({year_a} → {year_b})",
        threshold_scale=[vmin, vmin*0.75, vmin*0.5, vmin*0.25, 0, vmax*0.25, vmax*0.5, vmax*0.75, vmax]
    ).add_to(m)

# Tooltip & pop up
if selected_norm == "Percentage":
    tooltip_fields = ["community", "pct_A_fmt", "pct_B_fmt", "pct_change_fmt"]
    tooltip_aliases = [
        "Community",
        f"% in {year_a}",
        f"% in {year_b}",
        "Percent Change"
    ]
else:
    tooltip_fields = ["community", f"{selected_land_use}_A", f"{selected_land_use}_B", "area_change_fmt"]
    tooltip_aliases = [
        "Community",
        f"Area in {year_a} (sq mi)",
        f"Area in {year_b} (sq mi)",
        "Area % Change"
    ]

folium.GeoJson(
    merged,
    style_function=lambda x: {"fillOpacity": 0, "color": "black", "weight": 0.3},
    tooltip=folium.GeoJsonTooltip( tooltip_fields, tooltip_aliases, localize=True)
        
).add_to(m)



st_folium(m, width=700, height=500)