import json
import os

folder = "CMAP_Area_Count"

for filename in os.listdir(folder):
    if not filename.endswith(".geojson"):
        continue

    path = os.path.join(folder, filename)

    with open(path, "r") as f:
        data = json.load(f)

    for feature in data["features"]:
        props = feature["properties"]
        keys = list(props.keys())
        new_props = {}

        # First 7 metadata columns stay unchanged
        first_7 = keys[:7]

        for key in keys:
            value = props[key]

            # Keep metadata columns unchanged
            if key in first_7:
                new_props[key] = value
                continue

            # If key already has LANDUSE prefix → keep it
            if key.startswith("LANDUSE"):
                new_props[key] = value
                continue

            # If key is numeric (e.g., "1111") → add LANDUSE prefix
            if key.isdigit():
                new_props["LANDUSE" + key] = value
                continue

            # Otherwise keep as-is
            new_props[key] = value

        feature["properties"] = new_props

    with open(path, "w") as f:
        json.dump(data, f)

    print("✓ Cleaned", filename)


