import csv
import json
from pyproj import Transformer

def clean_str(value: str | None) -> str | None:
  if value is None:
      return None
  cleaned = " ".join(value.split())
  return cleaned if cleaned not in ("", "-") else None


def parse_int(value: str | None) -> int | None:
  cleaned = clean_str(value)
  if cleaned is None:
      return None
  try:
      return int(float(cleaned))
  except ValueError:
      return None

# Ορισμός μετατροπέα από Web Mercator (EPSG:3857) σε WGS84 (EPSG:4326)
transformer = Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True)

input_csv = 'public_parking.csv'       # Το αρχείο CSV εισόδου σας
output_geojson = 'public_parking.geojson'

features = []

with open(input_csv, mode='r', encoding='utf-8-sig') as f:
  reader = csv.DictReader(f)
  for row in reader:
    x_mercator = float(row["x"])
    y_mercator = float(row["y"])
    
    # Μετατροπή σε γεωγραφικές συντεταγμένες (lon, lat)
    lon, lat = transformer.transform(x_mercator, y_mercator)
    print(lon, lat)

    feature = {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [round(lon, 8), round(lat, 8)],
      },
      "properties": {
       "object_id": parse_int(row.get("OBJECTID")),
        "name": clean_str(row.get("Ονομασία")),
        "location": clean_str(row.get("Τοποθεσία")),
        "size": clean_str(row.get("Μέγεθος")),
        "spaces": clean_str(row.get("Θέσεις")),
      },
    }
    features.append(feature)

geojson_data = {
  "type": "FeatureCollection",
  "features": features
}

with open(output_geojson, mode='w', encoding='utf-8') as f:
  json.dump(geojson_data, f, ensure_ascii=False, indent=2)

print(f"Το αρχείο {output_geojson} δημιουργήθηκε με επιτυχία και οι συντεταγμένες μετατράπηκαν σωστά σε WGS84!")