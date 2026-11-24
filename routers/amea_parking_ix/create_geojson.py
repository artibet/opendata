import csv
import json
from pyproj import Transformer

def clean_text(value: str | None) -> str:
  if not value:
      return ""
  return " ".join(value.split())

# Ορισμός μετατροπέα από Web Mercator (EPSG:3857) σε WGS84 (EPSG:4326)
transformer = Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True)

input_csv = 'amea_parking_ix.csv'       # Το αρχείο CSV εισόδου σας
output_geojson = 'amea_parking_ix.geojson'

features = []

with open(input_csv, mode='r', encoding='utf-8-sig') as f:
  reader = csv.DictReader(f)
  for row in reader:
    x_mercator = float(row["x"])
    y_mercator = float(row["y"])
    
    # Μετατροπή σε γεωγραφικές συντεταγμένες (lon, lat)
    lon, lat = transformer.transform(x_mercator, y_mercator)

    object_id = int(row["OBJECTID"])
    location = clean_text(row["ΤΟΠΟΘΕΣΙΑ"])
    status = clean_text(row["ΚΑΤΑΣΤΑΣΗ"])
    parking_card = clean_text(row["ΚΑΡΤΑ ΣΤΑΘΜΕΥΣΗΣ"])

    feature = {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [lon, lat]  # Το GeoJSON απαιτεί [Longitude, Latitude]
      },
      "properties": {
        "object_id" : int(row["OBJECTID"]) if row["OBJECTID"].isdigit() else row["OBJECTID"],
        "location"  : location,
        "status"    : status,
        "parking_card": parking_card
      }
    }
    features.append(feature)

geojson_data = {
  "type": "FeatureCollection",
  "features": features
}

with open(output_geojson, mode='w', encoding='utf-8') as f:
  json.dump(geojson_data, f, ensure_ascii=False, indent=2)

print(f"Το αρχείο {output_geojson} δημιουργήθηκε με επιτυχία και οι συντεταγμένες μετατράπηκαν σωστά σε WGS84!")