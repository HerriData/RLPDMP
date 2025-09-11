import pandas as pd
import json
from datetime import datetime
import math

def clean_value(val):
    """Convertit NaN et inf en None"""
    if isinstance(val, float) and (math.isnan(val) or math.isinf(val)):
        return None
    return val

def clean_properties(d):
    """Applique clean_value à tous les champs du dictionnaire"""
    return {k: clean_value(v) for k, v in d.items()}

def main():
    df = pd.read_csv("data.csv")

    features = []
    for _, row in df.iterrows():
        if row["X"] is not None and row["Y"] is not None:
            properties = row.drop(["X", "Y"]).to_dict()
            properties = clean_properties(properties)  # 👈 conversion NaN -> None
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [row["X"], row["Y"]],
                },
                "properties": properties
            })

    geojson = {
        "type": "FeatureCollection",
        "features": features,
        "generated_at": datetime.utcnow().isoformat()
    }

    with open("data.geojson", "w", encoding="utf-8") as f:
        json.dump(geojson, f, indent=2, ensure_ascii=False)

    print(f"✅ Fichier data.geojson généré avec {len(features)} points.")

if __name__ == "__main__":
    main()
