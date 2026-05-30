import streamlit as st
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import altair as alt
import seaborn as sns

@st.cache_data
def load_geojson(path):
    gdf = gpd.read_file(path)
    gdf["community"] = gdf["community"].str.title()
    return gdf


# Year selection only
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

st.sidebar.header("Chart Controls")
selected_type = st.sidebar.selectbox("Select Data Type:", ["Parcel Area", "Parcel Count"])
if selected_type == "Parcel Area":
    selected_norm = st.sidebar.selectbox("Normalize By:", ["Square Miles", "Percentage"])
else:
    selected_norm = st.sidebar.selectbox("Normalize By:", ["Count", "Percentage"])
selected_year = st.sidebar.selectbox("Select Year:", list(files[selected_type].keys()))
gdf = load_geojson(files[selected_type][selected_year])

# Land use groups
land_use_columns = [
    'Single Family Residential', 'Multi-Family Residential', 'Commercial',
    'Urban Mix + Residential', 'Institutional', 'Industrial',
    'TCUW', 'Agricultural', 'Open Space', 'Vacant',
    'Under Construction', 'Water', 'Non-Parcel / Other'
]

#rename total for dropdowns
gdf.rename(columns={"Total": "All of Chicago"}, inplace=True)

# -------------------------
# COMMUNITY AREA DROPDOWN
# -------------------------
areas = ["All of Chicago"] + sorted(gdf["community"].unique().tolist())
selected_area = st.sidebar.selectbox("Select Community Area:", areas)

# -------------------------
# FILTER DATA FOR BAR + DONUT
# -------------------------
if selected_area == "All of Chicago":
    totals = gdf[land_use_columns].sum().sort_values(ascending=False)
else:
    row = gdf[gdf["community"] == selected_area].iloc[0]
    totals = row[land_use_columns].sort_values(ascending=False)

percentages = (totals / totals.sum()) * 100
square_miles = totals

# -------------------------
# BAR CHART
# -------------------------
if selected_norm == "Percentage":
    st.subheader(f"Land Use {selected_type} Percentage (%) Distribution in {selected_year} — {selected_area}")
elif selected_norm == "Count":
    st.subheader(f"Land Use {selected_type} Distribution in {selected_year} — {selected_area}")
else:
    st.subheader(f"Land Use {selected_type} Distribution in Square Miles in {selected_year} — {selected_area}")

fig1, ax1 = plt.subplots(figsize=(10, 6))
if selected_norm == "Percentage":
    percentages.plot(kind='bar', ax=ax1, color='skyblue')
    ax1.set_ylabel("Percentage of Total Land Use (%)")
    ax1.set_title(f"Land Use {selected_type} Percentages in {selected_area} ({selected_year})")
    ax1.set_ylim(0, percentages.max() * 1.15)

    for i, v in enumerate(percentages):
        ax1.text(i, v + 0.5, f"{v:.1f}%", ha='center', fontsize=9)
elif selected_norm == "Count":
    totals.plot(kind='bar', ax=ax1, color='lightgreen')
    ax1.set_ylabel(f"{selected_type} Count")
    ax1.set_title(f"Land Use {selected_type} Counts in {selected_area} ({selected_year})")
    ax1.set_ylim(0, totals.max() * 1.15)

    for i, v in enumerate(totals):
        ax1.text(i, v + (totals.max() * 0.01), f"{int(v):,}", ha='center', fontsize=9)

else:
    square_miles.plot(kind='bar', ax=ax1, color='salmon')
    ax1.set_ylabel(f"{selected_type} in Square Miles")
    ax1.set_title(f"Land Use {selected_type} in Square Miles in {selected_area} ({selected_year})")
    ax1.set_ylim(0, square_miles.max() * 1.15)

    for i, v in enumerate(square_miles):
        ax1.text(i, v + (square_miles.max() * 0.01), f"{v:.2f}", ha='center', fontsize=9)

plt.xticks(rotation=45, ha='right')
st.pyplot(fig1)

# -------------------------
# DONUT CHART
# -------------------------
st.subheader(f"{selected_norm} Breakdown")

fig2, ax2 = plt.subplots(figsize=(8, 8))
colors = cm.get_cmap('tab20')(np.linspace(0, 1, len(totals)))

if selected_norm == "Percentage":
    wedges, _ = ax2.pie(
        percentages,
        startangle=90,
        wedgeprops=dict(width=0.4),
        colors=colors
    )
elif selected_norm == "Count":
    wedges, _ = ax2.pie(
        totals,
        startangle=90,
        wedgeprops=dict(width=0.4),
        colors=colors
    )
else: 
    wedges, _ = ax2.pie(
        square_miles,
        startangle=90,
        wedgeprops=dict(width=0.4),
        colors=colors
)

if selected_norm == "Percentage":
    labels = [
        f"{label}: {pct:.1f}%" for label, pct in zip(totals.index, percentages)
    ]
elif selected_norm == "Count":
    labels = [
        f"{label}: {int(count):,}" for label, count in zip(totals.index, totals)
    ]
else:
    labels = [
        f"{label}: {sqmi:.2f}" for label, sqmi in zip(totals.index, square_miles)
    ]

ax2.legend(
    wedges,
    labels,
    title="Land Use Types",
    loc="center left",
    bbox_to_anchor=(1, 0.5),
    fontsize=10
)

centre_circle = plt.Circle((0, 0), 0.60, fc='white')
fig2.gca().add_artist(centre_circle)

ax2.set_ylabel("")
plt.tight_layout()
st.pyplot(fig2)

# -------------------------
# MULTI-YEAR TREND CHART
# -------------------------
st.subheader(f"Multi-Year Trend — {selected_norm} of {selected_type} in {selected_area}")

# Dropdown for land-use category
selected_lu = st.selectbox("Select Land Use Category for Trend:", land_use_columns)

# Build trend dataset
trend_records = []

for yr, path in files[selected_type].items():
    gdf_year = load_geojson(path)

    if selected_area == "All of Chicago":
        totals_year = gdf_year[land_use_columns].sum()
    else:
        row_year = gdf_year[gdf_year["community"] == selected_area].iloc[0]
        totals_year = row_year[land_use_columns]

    pct_year = (totals_year / totals_year.sum()) * 100
    square_miles_year = totals_year

    if selected_norm == "Percentage":
        trend_records.append({
            "Year": int(yr),
            "Percent": pct_year[selected_lu]
        })
    elif selected_norm == "Count":
        trend_records.append({
            "Year": int(yr),
            "Count": totals_year[selected_lu]
        })
    else:
        trend_records.append({
            "Year": int(yr),
            "Square Miles": square_miles_year[selected_lu]
        })

trend_df = pd.DataFrame(trend_records)

# Line chart
if selected_norm == "Percentage":
    y_encoding = alt.Y("Percent:Q", title=f"{selected_lu} Land Use (%)")
    tooltip_fields = ["Year", "Percent"]
elif selected_norm == "Count":
    y_encoding = alt.Y("Count:Q", title=f"{selected_lu} Parcel Count")
    tooltip_fields = ["Year", "Count"]
else:
    y_encoding = alt.Y("Square Miles:Q", title=f"{selected_lu} Area (Square Miles)")
    tooltip_fields = ["Year", "Square Miles"]

line_chart = alt.Chart(trend_df).mark_line(point=True).encode(
    y=y_encoding,
    x=alt.X("Year:O", title="Year"),
    tooltip=tooltip_fields,
).properties(
    width=800,
    height=400,
    title=f"{selected_lu} Trend Over Time — {selected_type} in {selected_area}"
)

if selected_norm == "Percentage":
    text = line_chart.mark_text(align='center', dx=5, dy=-15, stroke='black', strokeWidth=.5, fill='white', fontSize=14).encode(
        text=alt.Text("Percent:Q", format=".1f")
    )
elif selected_norm == "Count":
    text = line_chart.mark_text(align='center', dx=5, dy=-15, stroke='black', strokeWidth=.5, fill='white', fontSize=14).encode(
        text=alt.Text("Count:Q", format=",")
    )
else:
    text = line_chart.mark_text(align='center', dx=5, dy=-15, stroke='black', strokeWidth=.5, fill='white', fontSize=14).encode(
        text=alt.Text("Square Miles:Q", format=".2f")
    )

line_chart = line_chart + text

st.altair_chart(line_chart, use_container_width=True)

# correlation matrix
if selected_type == "Parcel Area":
    st.subheader(f"Correlation Matrix of Land Use Categories — {selected_type} (sq mi) in {selected_year}")
    plt.title(f"Correlation Matrix of Land Use Categories — {selected_type} (sq mi) in {selected_year}")
else:
    st.subheader(f"Correlation Matrix of Land Use Categories — {selected_type} in {selected_year}")
    plt.title(f"Correlation Matrix of Land Use Categories — {selected_type} in {selected_year}")
corr_matrix = gdf[land_use_columns].corr()
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, fmt=".2f", linewidths=0.5)
st.pyplot(plt)

# Box Plot
st.subheader(f"Box Plot — {selected_type} of Land Use Categories in {selected_year}")

box = gdf.melt(id_vars=["community"], value_vars=land_use_columns, var_name="Land Use", value_name="Value")
if selected_norm == "Percentage":
    box["Value"] = (box["Value"] / box["Value"].sum()) * 100
    box = alt.Chart(box).mark_boxplot().encode(
        x=alt.X("Land Use:N", title="Land Use Category"),
        y=alt.Y("Value:Q", title=f"{selected_type} (%)"),
        tooltip=["community", "Land Use", "Value", alt.Tooltip("Value", format=".2f")]
    ).properties(
        width=800,
        height=400,
        title=f"Box Plot of {selected_type} of Land Use Categories in {selected_year}"
    )
elif selected_norm == "Count":
    box = alt.Chart(box).mark_boxplot().encode(
        x=alt.X("Land Use:N", title="Land Use Category"),
        y=alt.Y("Value:Q", title=f"{selected_type} Count"),
        tooltip=["community", "Land Use", "Value", alt.Tooltip("Value", format=".2f")]
    ).properties(
        width=800,
        height=400,
        title=f"Box Plot of {selected_type} of Land Use Categories in {selected_year}"
    )
else:
    box = alt.Chart(box).mark_boxplot().encode(
        x=alt.X("Land Use:N", title="Land Use Category"),
        y=alt.Y("Value:Q", title=f"{selected_type} in Square Miles"),
        tooltip=["community", "Land Use", "Value", alt.Tooltip("Value", format=".2f")]
    ).properties(
        width=800,
        height=400,
        title=f"Box Plot of {selected_type} of Land Use Categories in {selected_year}"
    )

st.altair_chart(box, use_container_width=True)

# see table data
if selected_type == "Parcel Area":
    st.subheader(f"Data Table — {selected_type} (sq mi) in {selected_year}")
else:
    st.subheader(f"Data Table — {selected_type} in {selected_year}")

st.dataframe(gdf[["community"] + land_use_columns + ["All of Chicago"]].sort_values("community").reset_index(drop=True))