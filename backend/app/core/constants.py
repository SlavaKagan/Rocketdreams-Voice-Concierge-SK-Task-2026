# ── Semantic Search ────────────────────────────────────────────────────────────
SIMILARITY_THRESHOLD = 0.78
EMBEDDING_MODEL = "text-embedding-ada-002"
EMBEDDING_DIMENSIONS = 1536
EMBEDDING_RETRIES = 3
EMBEDDING_RETRY_DELAY = 1.0

# ── Voice ──────────────────────────────────────────────────────────────────────
DEFAULT_VOICE_ID = 1
ELEVENLABS_TTS_MODEL = "eleven_turbo_v2_5"
VOICE_PREVIEW_TEXT = (
    "Welcome to The Meridian Casino and Resort. "
    "How may I assist you this evening?"
)

# ── Playground ─────────────────────────────────────────────────────────────────
PLAYGROUND_ROOM = "meridian-playground"

# ── API ────────────────────────────────────────────────────────────────────────
API_VERSION = "1.0.0"
RATE_LIMIT_SEARCH = "30/minute"
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
]

# ── Database Connection Pool ───────────────────────────────────────────────────
DB_POOL_SIZE = 10
DB_MAX_OVERFLOW = 20
DB_POOL_RECYCLE = 3600

# ── HTTP Client ────────────────────────────────────────────────────────────────
HTTP_SEARCH_TIMEOUT = 10.0
HTTP_VOICE_TIMEOUT = 5.0
HTTP_RETRIES = 3
HTTP_RETRY_DELAY = 1.0

# ── Voices ─────────────────────────────────────────────────────────────────────
VOICES = {
    1: {
        "id": 1,
        "name": "James",
        "elevenlabs_id": "pNInz6obpgDQGcFmaJgB",
        "description": "Male, mature, warm British accent. Professional and refined."
    },
    2: {
        "id": 2,
        "name": "Sofia",
        "elevenlabs_id": "SUt4lKV5Yg2QPF7Bs3Ae",
        "description": "Female, friendly, subtle European accent. Welcoming and elegant."
    },
    3: {
        "id": 3,
        "name": "Marcus",
        "elevenlabs_id": "ErXwobaYiN019PkySvjV",
        "description": "Male, American, confident and energetic. Modern and approachable."
    },
    4: {
        "id": 4,
        "name": "Elena",
        "elevenlabs_id": "EXAVITQu4vr4xnSDxMaL",
        "description": "Female, American, calm and reassuring. Sophisticated and clear."
    },
}