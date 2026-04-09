def test_get_voices(client, db):
    from app.models.models import VoiceConfig
    config = VoiceConfig(active_voice_id=1)
    db.add(config)
    db.commit()

    response = client.get("/api/voices")
    assert response.status_code == 200
    data = response.json()
    assert "active_voice_id" in data
    assert "voices" in data
    assert len(data["voices"]) == 4

def test_set_active_voice(client, db):
    from app.models.models import VoiceConfig
    config = VoiceConfig(active_voice_id=1)
    db.add(config)
    db.commit()

    response = client.put("/api/voices/active", json={"voice_id": 2})
    assert response.status_code == 200
    assert response.json()["active_voice_id"] == 2

def test_set_invalid_voice(client):
    response = client.put("/api/voices/active", json={"voice_id": 99})
    assert response.status_code == 400

def test_voice_names(client, db):
    from app.models.models import VoiceConfig
    config = VoiceConfig(active_voice_id=1)
    db.add(config)
    db.commit()

    response = client.get("/api/voices")
    voices = response.json()["voices"]
    names = [v["name"] for v in voices]
    assert "James" in names
    assert "Sofia" in names
    assert "Marcus" in names
    assert "Elena" in names