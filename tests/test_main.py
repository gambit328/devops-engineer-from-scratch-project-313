from main import app


def test_ping():
    client = app.test_client()
    response = client.get("/ping")

    assert response.status_code == 200
    assert response.get_data(as_text=True) == "pong"


def test_get_links():
    client = app.test_client()
    response = client.get("/api/links")

    assert response.status_code == 200
    assert type(response.get_json()) == list
