# Semantic search
SIMILARITY_THRESHOLD = 0.78
EMBEDDING_MODEL = "text-embedding-ada-002"
EMBEDDING_DIMENSIONS = 1536

# Voice config
DEFAULT_VOICE_ID = 1

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

# Playground
PLAYGROUND_ROOM = "meridian-playground"