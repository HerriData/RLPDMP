import pandas as pd
import json
from datetime import datetime

def main():
    # 1. Lire le CSV téléchargé depuis Google Sheets
    df = pd.read_csv("data.csv")

    # 2. Remplacer tous les NaN par None pour JSON valide
    df = df.where(pd.notnull(df), None)

    features = []
    for _, row in df.iterrows():
        # Vérifier que les coordonnées existent
        if row["X"] is not None and row["Y"] is not None:
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [row["X"], row["Y"]],  # lon, lat
                },
                "properties": row.drop(["X", "Y"]).to_dict()
            })

    # 3. Création de la FeatureCollection
    geojson = {
        "type": "FeatureCollection",
        "features": features,
        "generated_at": datetime.utcnow().isoformat()  # champ dynamique
    }

    # 4. Sauvegarde en UTF-8
    with open("data.geojson", "w", encoding="utf-8") as f:
        json.dump(geojson, f, indent=2, ensure_ascii=False)

    print(f"✅ Fichier data.geojson généré avec {len(features)} points.")

if __name__ == "__main__":
    main()
