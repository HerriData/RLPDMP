import pandas as pd
import json

def main():
    # 1. Lire le CSV téléchargé depuis Google Sheets
    df = pd.read_csv("data.csv")

    # Remplacer tous les NaN/NaT par None (JSON -> null)
    df = df.where(pd.notnull(df), None)

    # 2. Conversion en GeoJSON
    features = []
    for _, row in df.iterrows():
        if "X" in row and "Y" in row:
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [row["X"], row["Y"]],
                },
                "properties": row.drop(["X", "Y"]).to_dict()
            })

    geojson = {"type": "FeatureCollection", "features": features}

    # 3. Sauvegarde en UTF-8 sans BOM
    with open("data.geojson", "w", encoding="utf-8") as f:
        json.dump(geojson, f, indent=2, ensure_ascii=False)

    print("✅ Fichier data.geojson généré avec", len(features), "points.")

if __name__ == "__main__":
    main()
