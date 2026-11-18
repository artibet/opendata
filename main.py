from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import root
from routers.amea_parking import router as amea_parking_router

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
