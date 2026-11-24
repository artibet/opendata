from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from pathlib import Path
import json

# Create the router
router = APIRouter(
  prefix='/loading-zones',
  tags=['loading-zones']  
)

BASE_DIR = Path.cwd()
GEOJSON_FILE = BASE_DIR / "routers/loading_zones/loading_zones.geojson"

@router.get('', status_code=200)
async def crosswalks():
  try:
    with open(GEOJSON_FILE, "r", encoding="utf-8") as f:
      data = json.load(f)
    return JSONResponse(content=data)
  except FileNotFoundError:
      raise HTTPException(status_code=404, detail="GeoJSON file not found")
  except json.JSONDecodeError:
      raise HTTPException(status_code=500, detail="Invalid GeoJSON format")
