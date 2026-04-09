from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import init_db
from app.core.logging import setup_logging
from app.routes import faqs, unanswered, voice, search

setup_logging()

app = FastAPI(
    title="Meridian Concierge API",
    version="1.0.0",
    description="Backend API for The Meridian Casino & Resort Voice Concierge"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(search.router)
app.include_router(faqs.router)
app.include_router(unanswered.router)
app.include_router(voice.router)

@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok", "service": "Meridian Concierge API"}