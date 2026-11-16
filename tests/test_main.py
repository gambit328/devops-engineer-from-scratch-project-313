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


def test_get_link():
    client = app.test_client()
    response = client.post(
        "/api/links",
        json={"original_url": "https://example.com/long-url", "short_name": "t2"},
    )
    assert response.status_code == 201
    created_data = response.get_json()

    response = client.get(f"/api/links/{created_data['id']}")
    data = response.get_json()

    response_error = client.get("/api/links/999999")
    data_error = response_error.get_json()

    assert response.status_code == 200
    assert "id" in data and "short_name" in data
    assert (
        created_data["id"] == data["id"]
        and created_data["short_name"] == data["short_name"]
    )
    assert response_error.status_code == 404
    assert "A link with this id does not exist" == data_error["detail"]

    client.delete(f"/api/links/{data['id']}")
