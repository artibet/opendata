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

input_csv = 'bus_stops.csv'       # Το αρχείο CSV εισόδου σας
output_geojson = 'bus_stops.geojson'

features = []

ROUTE_COLUMNS = [
  "F1AT", "F1TA", "F2AT", "F2TA", "F4AT", "F4TA", "F5AT", "F5TA",
  "F9AT", "F9TA", "F10AT", "F10TA", "F14AT", "F14TA", "F15AT", "F15TA",
  "F16AT", "F16TA", "F17AT", "F17TA", "F18AT", "F18TA", "F20AT", "F20TA",
  "F13AT", "F13TA", "F23AT", "F23TA", "F29AT", "F29TA",
]

with open(input_csv, mode='r', encoding='utf-8-sig') as f:
  reader = csv.DictReader(f)
  for row in reader:
    x_mercator = float(row["x"])
    y_mercator = float(row["y"])
    
    # Μετατροπή σε γεωγραφικές συντεταγμένες (lon, lat)
    lon, lat = transformer.transform(x_mercator, y_mercator)
    print(lon, lat)

    route_flags = {}
    active_routes = []
    for col in ROUTE_COLUMNS:
      val = parse_int(row.get(col))
      route_flags[col.lower()] = val
      if val == 1:
        active_routes.append(col)

    feature = {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [round(lon, 8), round(lat, 8)],
      },
      "properties": {
        "object_id": parse_int(row.get("OBJECTID")),
        "name": clean_str(row.get("ΟΝΟΜΑΣΙΑ")),
        "vms": parse_int(row.get("VMS")),
        "starts": parse_int(row.get("Starts")),
        "routes": active_routes,
        **route_flags,
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