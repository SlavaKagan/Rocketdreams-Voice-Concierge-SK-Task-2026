def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_search_no_match_records_unanswered(client, mocker):
    mocker.patch(
        "app.routes.search.get_embedding",
        return_value=[0.1] * 1536
    )
    mocker.patch(
        "app.repositories.faq.search_by_embedding",
        return_value=None
    )

    response = client.post("/api/search", json={"query": "Can I bring my cat?"})
    assert response.status_code == 200
    assert response.json()["found"] == False

    # Verify it was recorded as unanswered
    unanswered = client.get("/api/unanswered")
    questions = unanswered.json()
    assert any(q["question"] == "Can I bring my cat?" for q in questions)

def test_search_with_match(client, mocker):
    mocker.patch(
        "app.routes.search.get_embedding",
        return_value=[0.1] * 1536
    )

    from unittest.mock import MagicMock
    mock_row = MagicMock()
    mock_row.question = "Is the poker room open?"
    mock_row.answer = "Yes, our poker room is open 24/7."
    mock_row.category = "Gaming"

    mocker.patch(
        "app.repositories.faq.search_by_embedding",
        return_value=(mock_row, 0.95)
    )

    response = client.post("/api/search", json={"query": "Is poker room open?"})
    assert response.status_code == 200
    data = response.json()
    assert data["found"] == True
    assert data["answer"] == "Yes, our poker room is open 24/7."
    assert data["similarity"] == 0.95