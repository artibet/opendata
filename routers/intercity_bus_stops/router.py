from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from pathlib import Path
import json

# Create the router
router = APIRouter(
  prefix='/intercity-bus-stops',
  tags=['intercity-bus-stops']  
)

BASE_DIR = Path.cwd()
GEOJSON_FILE = BASE_DIR / "routers/intercity_bus_stops/intercity_bus_stops.geojson"

@router.get('', status_code=200)
async def intercity_bus_stops():
  try:
    with open(GEOJSON_FILE, "r", encoding="utf-8") as f:
      data = json.load(f)
    return JSONResponse(content=data)
  except FileNotFoundError:
      raise HTTPException(status_code=404, detail="GeoJSON file not found")
  except json.JSONDecodeError:
      raise HTTPException(status_code=500, detail="Invalid GeoJSON format")
