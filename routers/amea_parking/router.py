from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from pathlib import Path
import json

# Create the router
router = APIRouter(
  prefix='/amea-parking',
  tags=['amea-parking']  
)

BASE_DIR = Path.cwd()
GEOJSON_FILE = BASE_DIR / "routers/amea_parking/amea.geojson"

@router.get('', status_code=200)
async def amea_parking():
  try:
    with open(GEOJSON_FILE, "r", encoding="utf-8") as f:
      data = json.load(f)
    return JSONResponse(content=data)
  except FileNotFoundError:
      raise HTTPException(status_code=404, detail="Amea GeoJSON file not found")
  except json.JSONDecodeError:
      raise HTTPException(status_code=500, detail="Invalid GeoJSON format")
