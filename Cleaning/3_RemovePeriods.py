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
        new_props = {}

        for key, value in props.items():
            # Replace dots with underscores
            new_key = key.replace(".", "_")
            new_props[new_key] = value

        feature["properties"] = new_props

    with open(path, "w") as f:
        json.dump(data, f)

    print("✓ Cleaned", filename)
