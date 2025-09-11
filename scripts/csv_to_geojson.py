import csv
import json
import os

def main():
    features = []
    csv_file = "data.csv"

    with open(csv_file, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader, start=1):
            try:
                x = float(row.get("X", "").strip() or 0)
                y = float(row.get("Y", "").strip() or 0)
            except ValueError:
                continue  # ignorer les lignes invalides

            # Construire les propriétés (tout sauf X et Y)
            props = {k: (v if v != "" else None) for k, v in row.items() if k not in ("X", "Y")}
            props["ID"] = i

            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [x, y],
                },
                "properties": props,
            })

    geojson = {"type": "FeatureCollection", "features": features}

    with open("data.geojson", "w", encoding="utf-8") as f:
        json.dump(geojson, f, indent=2, ensure_ascii=False)

    print(f"✅ Fichier data.geojson généré avec {len(features)} points.")

    # --- Supprimer le CSV après usage ---
    try:
        os.remove(csv_file)
        print(f"✅ Fichier {csv_file} supprimé après traitement.")
    except FileNotFoundError:
        print(f"⚠️ Fichier {csv_file} non trouvé pour suppression.")

if __name__ == "__main__":
    main()