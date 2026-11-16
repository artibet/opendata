from fastapi import APIRouter
from fastapi import Response

# Create the router
router = APIRouter(
  prefix='',
  tags=['root']  
)

# -----------------------------------------------------------------------------
# Test api
# -----------------------------------------------------------------------------
@router.get('/', status_code=200)
async def root():
  return {"message": "Open Data API is live!", "status": "active"}

# -----------------------------------------------------------------------------
# No favicon response
# -----------------------------------------------------------------------------
@router.get('/favicon.ico', include_in_schema=False)
async def favicon():
  return Response(status_code=204)