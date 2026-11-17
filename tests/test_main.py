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


def test_put_link():
    client = app.test_client()
    response = client.post(
        "/api/links",
        json={"original_url": "https://example.com/long-url", "short_name": "t3"},
    )
    assert response.status_code == 201

    result = {
        "original_url": "https://example1.com/long-url",
        "short_name": "t3-update",
    }
    created_data = response.get_json()
    response = client.put(
        f"/api/links/{created_data['id']}",
        json=result,
    )
    created_data_update = response.get_json()

    assert response.status_code == 200
    assert created_data["id"] == created_data_update["id"]
    assert result["original_url"] == created_data_update["original_url"]
    assert result["short_name"] == created_data_update["short_name"]

    client.delete(f"/api/links/{created_data['id']}")


def test_put_link_404():
    client = app.test_client()
    response = client.put(
        "/api/links/9999999",
        json={"original_url": "https://example.com/long-url", "short_name": "t5"},
    )
    assert response.status_code == 404


def test_put_link_wrong_body():
    client = app.test_client()
    response = client.post(
        "/api/links",
        json={
            "original_url": "https://example.com/long-url",
            "short_name": "t6",
        },
    )
    assert response.status_code == 201

    created_data = response.get_json()
    response_wrong_type_body = client.put(
        f"/api/links/{created_data['id']}", json="wrong type body"
    )
    data_wrong_type_body = response_wrong_type_body.get_json()

    response_wrong_original_url = client.put(
        f"/api/links/{created_data['id']}", json={"short_name": "t6-update"}
    )
    data_wrong_original_url = response_wrong_original_url.get_json()

    response_wrong_short_name = client.put(
        f"/api/links/{created_data['id']}",
        json={
            "original_url": "https://example-update.com/long-url",
        },
    )
    data_wrong_short_name = response_wrong_short_name.get_json()

    assert response_wrong_type_body.status_code == 422
    assert data_wrong_type_body["detail"] == [{"type": "type of data is wrong"}]

    assert response_wrong_original_url.status_code == 422
    assert data_wrong_original_url["detail"] == [{"original_url": "missing"}]

    assert response_wrong_short_name.status_code == 422
    assert data_wrong_short_name["detail"] == [{"short_name": "missing"}]

    client.delete(f"/api/links/{created_data['id']}")


def test_put_link_double():
    client = app.test_client()
    response1 = client.post(
        "/api/links",
        json={
            "original_url": "https://example1.com/long-url",
            "short_name": "t7",
        },
    )
    assert response1.status_code == 201

    response2 = client.post(
        "/api/links",
        json={
            "original_url": "https://example2.com/long-url",
            "short_name": "t8",
        },
    )
    assert response2.status_code == 201

    created_data1 = response1.get_json()
    created_data2 = response2.get_json()

    response_double = client.put(
        f"/api/links/{created_data2['id']}",
        json={"original_url": "https://example3.com/long-url", "short_name": "t7"},
    )
    data_double = response_double.get_json()

    assert response_double.status_code == 422
    assert data_double["detail"] == "short_name already exists"

    client.delete(f"/api/links/{created_data1['id']}")
    client.delete(f"/api/links/{created_data2['id']}")
