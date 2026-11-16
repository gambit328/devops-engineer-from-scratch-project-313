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


def test_post_links():
    client = app.test_client()
    response = client.post(
        "/api/links",
        json={"original_url": "https://example.com/long-url", "short_name": "t1"},
    )
    data = response.get_json()

    assert response.status_code == 201
    assert "id" in data and "short_name" in data

    client.delete(f"/api/links/{data['id']}")
