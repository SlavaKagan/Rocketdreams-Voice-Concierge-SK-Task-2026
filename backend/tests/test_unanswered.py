def test_get_unanswered_empty(client):
    response = client.get("/api/unanswered")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_record_and_get_unanswered(client, mocker):
    mocker.patch(
        "app.routes.search.get_embedding",
        return_value=[0.1] * 1536
    )
    mocker.patch(
        "app.repositories.faq.search_by_embedding",
        return_value=None
    )
    client.post("/api/search", json={"query": "Can I bring my pet?"})

    response = client.get("/api/unanswered")
    assert response.status_code == 200
    questions = response.json()
    assert any(q["question"] == "Can I bring my pet?" for q in questions)

def test_dismiss_question(client, db):
    from app.models.models import UnansweredQuestion
    question = UnansweredQuestion(question="Dismiss me test")
    db.add(question)
    db.commit()
    db.refresh(question)

    response = client.delete(f"/api/unanswered/{question.id}/dismiss")
    assert response.status_code == 204

def test_dismiss_not_found(client):
    response = client.delete("/api/unanswered/99999/dismiss")
    assert response.status_code == 404

def test_frequency_increments(client, db):
    from app.models.models import UnansweredQuestion
    question = UnansweredQuestion(question="Repeated question test", frequency=1)
    db.add(question)
    db.commit()

    from app.repositories.unanswered import record
    record(db, "Repeated question test")

    db.refresh(question)
    assert question.frequency == 2