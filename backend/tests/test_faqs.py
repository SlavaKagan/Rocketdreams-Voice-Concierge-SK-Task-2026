def test_get_faqs_empty(client):
    response = client.get("/api/faqs")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_faq(client, mocker):
    mocker.patch(
        "app.routes.faqs.get_embedding",
        return_value=[0.1] * 1536
    )
    response = client.post("/api/faqs", json={
        "question": "What are the casino hours?",
        "answer": "The casino is open 24/7.",
        "category": "General"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["question"] == "What are the casino hours?"
    assert data["answer"] == "The casino is open 24/7."
    assert "id" in data

def test_update_faq(client, mocker):
    mocker.patch(
        "app.routes.faqs.get_embedding",
        return_value=[0.1] * 1536
    )
    create = client.post("/api/faqs", json={
        "question": "Test question",
        "answer": "Test answer",
        "category": "General"
    })
    faq_id = create.json()["id"]

    response = client.put(f"/api/faqs/{faq_id}", json={
        "answer": "Updated answer"
    })
    assert response.status_code == 200
    assert response.json()["answer"] == "Updated answer"

def test_delete_faq(client, mocker):
    mocker.patch(
        "app.routes.faqs.get_embedding",
        return_value=[0.1] * 1536
    )
    create = client.post("/api/faqs", json={
        "question": "To be deleted",
        "answer": "Delete me",
        "category": "General"
    })
    faq_id = create.json()["id"]

    response = client.delete(f"/api/faqs/{faq_id}")
    assert response.status_code == 204

def test_delete_faq_not_found(client):
    response = client.delete("/api/faqs/99999")
    assert response.status_code == 404

def test_update_faq_not_found(client):
    response = client.put("/api/faqs/99999", json={"answer": "x"})
    assert response.status_code == 404