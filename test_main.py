from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"


def test_latest_items():
    response = client.get("/items/latest")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"


def test_read_item():
    response = client.get("/items/1")
    if(response.status_code == 200):
        assert response.headers["content-type"] == "application/json"
        assert response.json() == {"id": 1, "title": "Hello World",
                                   "content": "This is my first post", "published": True, "rating": 5}
    else:
        assert response.status_code == 404
        assert response.headers["content-type"] == "application/json"


def test_create_item():
    response = client.post("/items/", json={"title": "Hello World",
                           "content": "This is my test post", "published": True, "rating": 5})
    if (response.status_code == 201):
        assert response.headers["content-type"] == "application/json"
    else:
        assert response.status_code == 422
        assert response.headers["content-type"] == "application/json"


def test_update_item():
    response = client.put(
        "/items/1", json={"title": "Hello World", "content": "updated", "published": True, "rating": 5})
    if (response.status_code == 200):
        assert response.headers["content-type"] == "application/json"
        assert response.json() == {"data": {"title": "Hello World",
                                   "content": "updated", "published": True, "rating": 5, "id": 1}}
    else:
        assert response.status_code == 422
        assert response.headers["content-type"] == "application/json"


def test_delete_item():
    response = client.delete("/items/1")
    if (response.status_code == 204):
        assert response.content == b"Item deleted"
    else:
        assert response.status_code == 404
