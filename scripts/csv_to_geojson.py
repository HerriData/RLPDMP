import pandas as pd
import json

def main():
    # 1. Lire le CSV téléchargé depuis Google Sheets
    df = pd.read_csv("data.csv")

    # 2. Conversion en GeoJSON
    features = []
    for _, row in df.iterrows():
        # Vérifie que les colonnes X et Y existent et sont valides
        if pd.notna(row.get("X")) and pd.notna(row.get("Y")):
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [row["X"], row["Y"]],  # X = longitude, Y = latitude
                },
                "properties": row.drop(["X", "Y"]).to_dict()  # tout le reste comme propriétés
            })

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    # 3. Sauvegarde
    with open("data.geojson", "w", encoding="utf-8") as f:
        json.dump(geojson, f, indent=2, ensure_ascii=False)

    print(f"✅ Fichier data.geojson généré avec {len(features)} points.")

if __name__ == "__main__":
    main()
