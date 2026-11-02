def register_user(client, username):

    return client.post(
        "/signup",
        json={
            "username": username,
            "email": f"{username}@example.com",
            "password": "Password123!"
        }
    )


def test_create_note(client):

    register_user(client, "alex")

    response = client.post(
        "/notes",
        json={
            "title": "My first note",
            "content": "Learning Flask",
            "category": "Education",
            "is_completed": False
        }
    )

    assert response.status_code == 201


def test_get_notes(client):

    register_user(client, "alex")

    client.post(
        "/notes",
        json={"title": "First note"}
    )

    response = client.get("/notes?page=1&per_page=5")

    assert response.status_code == 200
    assert response.get_json()["pagination"]["total"] == 1


def test_update_note(client):

    register_user(client, "alex")

    note = client.post(
        "/notes",
        json={"title": "Original title"}
    ).get_json()

    response = client.patch(
        f"/notes/{note['id']}",
        json={"title": "Updated title"}
    )

    assert response.status_code == 200
    assert response.get_json()["title"] == "Updated title"


def test_delete_note(client):

    register_user(client, "alex")

    note = client.post(
        "/notes",
        json={"title": "Delete me"}
    ).get_json()

    response = client.delete(f"/notes/{note['id']}")

    assert response.status_code == 200


def test_notes_require_authentication(client):

    assert client.get("/notes").status_code == 401


def test_user_cannot_access_another_users_notes(client):

    register_user(client, "alex")

    note = client.post(
        "/notes",
        json={"title": "Private note"}
    ).get_json()

    client.delete("/logout")

    register_user(client, "sam")

    response = client.get(f"/notes/{note['id']}")

    assert response.status_code == 404