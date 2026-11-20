import pytest

from main import app


@pytest.fixture
def make_link():
    created_links = []
    client = app.test_client()

    def _make(short_name, original_url="https://example.com/long-url"):
        response = client.post(
            "/api/links", json={"original_url": original_url, "short_name": short_name}
        )

        assert response.status_code == 201

        data = response.get_json()
        created_links.append(data)

        return data

    yield _make

    for elem in created_links:
        client.delete(f"/api/links/{elem['id']}")


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


def test_get_links_with_range(make_link):
    client = app.test_client()

    for i in range(15):
        make_link(f"p{i}")

    response = client.get("/api/links")
    assert response.status_code == 200
    all_links = response.get_json()

    response = client.get("/api/links?range=[5,10]")
    assert response.status_code == 200
    part_links = response.get_json()

    assert all_links[5:10] == part_links
    assert response.headers.get("Content-Range") == f"links 5-10/{len(all_links)}"


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


def test_get_link(make_link):
    client = app.test_client()
    created_data = make_link("t2")
    response = client.get(f"/api/links/{created_data['id']}")
    data = response.get_json()

    assert response.status_code == 200
    assert "id" in data and "short_name" in data
    assert (
        created_data["id"] == data["id"]
        and created_data["short_name"] == data["short_name"]
    )


def test_get_link_404():
    client = app.test_client()
    response = client.get("/api/links/9999999")
    data = response.get_json()

    assert response.status_code == 404
    assert "A link with this id does not exist" == data["detail"]


def test_put_link(make_link):
    client = app.test_client()
    result = {
        "original_url": "https://example1.com/long-url",
        "short_name": "t3-update",
    }
    created_data = make_link("t3")

    response = client.put(
        f"/api/links/{created_data['id']}",
        json=result,
    )
    created_data_update = response.get_json()

    assert response.status_code == 200
    assert created_data["id"] == created_data_update["id"]
    assert result["original_url"] == created_data_update["original_url"]
    assert result["short_name"] == created_data_update["short_name"]


def test_put_link_404():
    client = app.test_client()
    response = client.put(
        "/api/links/9999999",
        json={"original_url": "https://example.com/long-url", "short_name": "t5"},
    )
    assert response.status_code == 404


def test_put_link_wrong_body(make_link):
    client = app.test_client()
    created_data = make_link("t6")

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


def test_put_link_double(make_link):
    client = app.test_client()
    created_data1 = make_link("t7")
    created_data2 = make_link("t8")

    response_double = client.put(
        f"/api/links/{created_data2['id']}",
        json={
            "original_url": "https://example3.com/long-url",
            "short_name": created_data1["short_name"],
        },
    )
    data_double = response_double.get_json()

    assert response_double.status_code == 422
    assert data_double["detail"] == "short_name already exists"


def test_delete_link(make_link):
    client = app.test_client()
    created_data = make_link("t9")

    response = client.delete(f"/api/links/{created_data['id']}")

    assert response.status_code == 204
    assert response.get_data() == b""


def test_delete_link_404():
    client = app.test_client()
    response = client.delete("/api/links/99999999")
    data = response.get_json()

    assert response.status_code == 404
    assert "The link does not exist" == data["detail"]


def test_get_short_name(make_link):
    client = app.test_client()
    data = make_link("t10")
    response = client.get(f"/r/{data['short_name']}")
    headers_location = response.headers["Location"]

    assert response.status_code == 302
    assert data["original_url"] == headers_location


def test_get_short_name_404():
    client = app.test_client()
    response = client.get("/r/t11")
    data = response.get_json()

    assert response.status_code == 404
    assert "Link with the short_name does not exist" == data["detail"]
