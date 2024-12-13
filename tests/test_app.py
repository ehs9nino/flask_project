from app import app
import sys
import os
import pytest
import json

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def reset_users_file():
    """Reset the `users.txt` file before each test."""
    with open("users.txt", "w") as file:
        json.dump([], file)


def test_add_user(client):
    response = client.post('/add_user', json={"email": "test@example.com", "age": 30})
    assert response.status_code == 201
    assert response.json["message"] == "User added successfully!"


def test_get_user(client):
    client.post('/add_user', json={"email": "test2@example.com", "age": 25})
    response = client.get('/get_user', query_string={"email": "test2@example.com"})
    assert response.status_code == 200
    assert response.json["email"] == "test2@example.com"


def test_update_user(client):
    client.post('/add_user', json={"email": "test3@example.com", "age": 20})
    response = client.put('/update_user', json={"email": "test3@example.com", "age": 35})
    assert response.status_code == 200
    assert response.json["message"] == "User updated successfully!"
    assert response.json["user"]["age"] == 35


def test_delete_user(client):
    client.post('/add_user', json={"email": "test4@example.com", "age": 40})
    response = client.delete('/delete_user', json={"email": "test4@example.com"})
    assert response.status_code == 200
    assert response.json["message"] == "User deleted successfully!"
