from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import stories

app = FastAPI(title="Wanderlust API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://wanderlust-frontend-wot5c6gzla-ew.a.run.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stories.router, prefix="/api/stories", tags=["stories"])

import time
from datetime import datetime

START_TIME = time.time()

@app.get("/health")
def health_check():
    uptime = int(time.time() - START_TIME)
    return {
        "status": "ok",
        "service": "wanderlust-backend",
        "version": "1.0.0",
        "uptime_seconds": uptime,
        "timestamp": datetime.utcnow().isoformat()
    }