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


def parse_number(value: str | None) -> int | float | None:
  cleaned = clean_str(value)
  if cleaned is None:
    return None
  try:
    num = float(cleaned.replace(",", "."))
    return int(num) if num.is_integer() else num
  except ValueError:
    return None

# Ορισμός μετατροπέα από Web Mercator (EPSG:3857) σε WGS84 (EPSG:4326)
transformer = Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True)

input_csv = 'loading_zones.csv'       # Το αρχείο CSV εισόδου σας
output_geojson = 'loading_zones.geojson'

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
        "location": clean_str(row.get("Τοποθεσία")),
        "city_block": clean_str(row.get("OT")),
        "intersection": clean_str(row.get("Διασταύρωση")),
        "length": parse_number(row.get("Μήκος")),
        "spaces": parse_int(row.get("Θέσεις")),
        "decision": clean_str(row.get("Απόφαση")),
        "decision": clean_str(row.get("Ημερομηνία")),
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