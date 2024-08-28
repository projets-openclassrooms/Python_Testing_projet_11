import pytest
from server import app, clubs


@pytest.fixture
def client():
    return app.test_client()


def test_index(client):

    response = client.get("/")
    assert response.status == '200 OK'
    assert b"Dashboard Club points" in response.data


def test_show_summary_post(client):
    response = client.post("/showSummary", data={"email": clubs[0]["email"]})
    assert response.status == '200 OK'
    assert b"Welcome" in response.data
    assert b"Points available" in response.data


def test_show_summary_get_without_session(client):
    response = client.get("/showSummary")
    assert response.status == '405 METHOD NOT ALLOWED'
    assert b"Dashboard Club points" in client.get("/").data


def test_display_points(client):
    response = client.get("/dashboard")
    assert response.status == '200 OK'
    assert b"Points Display Board | GUDLFT Registration" in response.data
    for club in clubs:
        assert bytes(club["name"], "utf-8") in response.data
        assert bytes(str(club["points"]), "utf-8") in response.data


def test_logout(client):
    with client.session_transaction() as session:
        session["club_email"] = clubs[0]["email"]
    response = client.get("/logout")
    assert response.status == '302 FOUND'  # "GET /logout HTTP/1.1" 302
    assert b"Welcome to the GUDLFT Registration Portal!" in client.get("/").data
