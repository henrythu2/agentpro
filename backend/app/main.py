from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import clustering

app = FastAPI(title="Text Clustering API")

# Disable CORS. Do not remove this for full-stack development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(clustering.router, prefix="/api")

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}
