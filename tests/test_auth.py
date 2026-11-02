def signup(client):

    return client.post(
        "/signup",
        json={
            "username": "alex",
            "email": "alex@example.com",
            "password": "Password123!"
        }
    )


def test_signup(client):

    response = signup(client)

    assert response.status_code == 201
    assert response.get_json()["username"] == "alex"


def test_check_session(client):

    signup(client)

    response = client.get("/check_session")

    assert response.status_code == 200


def test_duplicate_signup(client):

    signup(client)

    response = signup(client)

    assert response.status_code == 409


def test_login(client):

    signup(client)
    client.delete("/logout")

    response = client.post(
        "/login",
        json={
            "username": "alex",
            "password": "Password123!"
        }
    )

    assert response.status_code == 200


def test_logout(client):

    signup(client)

    response = client.delete("/logout")

    assert response.status_code == 200

    assert client.get("/check_session").status_code == 401


def test_wrong_password(client):

    signup(client)
    client.delete("/logout")

    response = client.post(
        "/login",
        json={
            "username": "alex",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401