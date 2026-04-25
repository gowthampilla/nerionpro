import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.routes import router as api_router
from core.database import engine, Base

# Absolute path setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Initialize DB
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Nerion MVP")

# 1. API Routes first
app.include_router(api_router, prefix="/api/v1")

# 2. Static Dashboard second (Mounting to the ROOT '/')
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")

@app.get("/health")
def health_check():
    return {"status": "operational", "system": "nerion-core"}