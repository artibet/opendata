from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import root

# routers
from routers.amea_parking import router as amea_parking_router
from routers.schools import router as schools_router
from routers.crosswalks import router as crosswalks_router
from routers.amea_parking_ix import router as amea_parking_ix_router
from routers.bicycles import router as bicycles_router
from routers.loading_zones import router as loading_zones_router
from routers.public_parking import router as public_parking_router

# Load environment variables from .env
load_dotenv()

# Create and initialize fastapi application
app = FastAPI()
origins = [
  "*",
  # "http://localhost:9000",
  # "http://127.0.0.1:9000",
  # "http://127.0.0.1:9000",
]
app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"]
)

# Include the routers (endpoint groups)
app.include_router(root.router)
app.include_router(amea_parking_router.router)
app.include_router(schools_router.router)
app.include_router(crosswalks_router.router)
app.include_router(amea_parking_ix_router.router)
app.include_router(bicycles_router.router)
app.include_router(loading_zones_router.router)
app.include_router(public_parking_router.router)
