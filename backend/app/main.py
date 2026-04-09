from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import init_db
from app.routes import faqs, unanswered, voice, search

app = FastAPI(title="Meridian Concierge API", version="1.0.0")

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

app.include_router(faqs.router, prefix="/api")
app.include_router(unanswered.router, prefix="/api")
app.include_router(voice.router, prefix="/api")
app.include_router(search.router, prefix="/api")

@app.get("/health")
def health():
    return {"status": "ok", "service": "Meridian Concierge API"}