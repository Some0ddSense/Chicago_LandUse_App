import streamlit as st
import geopandas as gpd
import folium
from folium import plugins
from streamlit_folium import st_folium
import pandas as pd

@st.cache_data
def load_geojson(path):
    gdf = gpd.read_file(path)
    gdf["community"] = gdf["community"].str.title()
    return gdf


# Available years
files = {
    "Parcel Area": {
        '2023': 'CMAP_Area_Count/LUI_2023_Area.geojson',
        '2020': 'CMAP_Area_Count/LUI_2020_Area.geojson',
        '2015': 'CMAP_Area_Count/LUI_2015_Area.geojson',
        '2010': 'CMAP_Area_Count/LUI_2010_Area.geojson',
        '2005': 'CMAP_Area_Count/LUI_2005_Area.geojson',
        '2001': 'CMAP_Area_Count/LUI_2001_Area.geojson',
        '1990': 'CMAP_Area_Count/LUI_1990_Area.geojson'
    },
    "Parcel Count": {
        '2023': 'CMAP_Area_Count/LUI_2023_Count.geojson',
        '2020': 'CMAP_Area_Count/LUI_2020_Count.geojson',
        '2015': 'CMAP_Area_Count/LUI_2015_Count.geojson',
        '2010': 'CMAP_Area_Count/LUI_2010_Count.geojson',
        '2005': 'CMAP_Area_Count/LUI_2005_Count.geojson',
        '2001': 'CMAP_Area_Count/LUI_2001_Count.geojson',
        '1990': 'CMAP_Area_Count/LUI_1990_Count.geojson'
    }
}


# Sidebar controls
st.sidebar.header("Map Controls")
selected_type = st.sidebar.selectbox("Select Data Type:", ["Parcel Area", "Parcel Count"])
selected_year = st.sidebar.selectbox("Select Year:", list(files[selected_type].keys()))

# Load data
gdf = load_geojson(files[selected_type][selected_year])



# Ensure numeric types for all land use columns
land_use_columns = [
    'Single Family Residential', 'Multi-Family Residential', 'Commercial',
    'Urban Mix + Residential', 'Institutional', 'Industrial',
    'TCUW', 'Agricultural', 'Open Space', 'Vacant',
    'Under Construction', 'Water', 'Non-Parcel / Other', 'Total'
]

for col in land_use_columns:
    gdf[col] = pd.to_numeric(gdf[col], errors='coerce')

# Sidebar land use selector
selected_land_use = st.sidebar.selectbox("Select Land Use Group:", land_use_columns[:-1])  # exclude Total

# Compute percentage
gdf["percent_land_use"] = (gdf[selected_land_use] / gdf["Total"]) * 100
gdf["percent_land_use"] = gdf["percent_land_use"].fillna(0)

# Convert to square miles for tooltip display
if selected_type == "Parcel Area":
    gdf["square_miles"] = gdf[selected_land_use]

# App title and header
st.header(f"Percentage of {selected_land_use} {selected_type} by Chicago Community Area in {selected_year}")

# Fix invalid geometries before centroids
gdf["geometry"] = gdf["geometry"].buffer(0)

# Create map
center_lat = gdf.geometry.centroid.y.mean()
center_lon = gdf.geometry.centroid.x.mean()
m = folium.Map(location=[center_lat, center_lon], zoom_start=10, min_zoom=9, tiles='Cartodb.voyagernolabels')



# Add choropleth (percentage map)
folium.Choropleth(
    geo_data=gdf.to_json(),
    data=gdf,
    columns=['BoundsP_area_numbe', 'percent_land_use'],
    key_on='properties.BoundsP_area_numbe',
    fill_color='PuBuGn',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name=f"{selected_land_use} {selected_type} (% of total land use)",
    nan_fill_color='white'
).add_to(m)

# Add hover tooltip
folium.GeoJson(
    gdf,
    style_function=lambda feature: {
        'fillOpacity': 0,
        'color': 'black',
        'weight': 0.3   # <-- thinner outlines
    },
    tooltip=folium.GeoJsonTooltip(
        fields=['community', 'percent_land_use', 'square_miles'] if selected_type == "Parcel Area" else ['community', 'percent_land_use'],
        aliases=['Community', f'{selected_land_use} (%)', f"Land Use Square Miles"] if selected_type == "Parcel Area" else ['Community', f'{selected_land_use} (%)'],
        localize=True
    )
).add_to(m)


st_folium(m, width=700, height=500)