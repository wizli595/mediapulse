from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dashboard.backend.routes import articles, sources, stats, topics, trends

app = FastAPI(
    title="MediaPulse API",
    description="Analytics API for the MediaPulse news platform",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stats.router, prefix="/api")
app.include_router(articles.router, prefix="/api")
app.include_router(trends.router, prefix="/api")
app.include_router(topics.router, prefix="/api")
app.include_router(sources.router, prefix="/api")


@app.get("/health")
def health():
    return {"status": "ok"}
