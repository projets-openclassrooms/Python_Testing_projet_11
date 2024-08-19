import pytest
from server import app, clubs


@pytest.fixture
def client():
    return app.test_client()


def test_index(client):

    response = client.get("/")
    assert response.status == '200 OK'
    assert b"See the dashboard clubs points" in response.data


def test_show_summary_post(client):
    response = client.post("/showSummary", data={"email": clubs[0]["email"]})
    assert response.status == '200 OK'
    assert b"Welcome" in response.data
    assert b"Points available" in response.data


def test_show_summary_get_without_session(client):
    response = client.get("/showSummary")
    assert response.status == '302 Found'
    assert b"See the dashboard clubs points" in client.get("/").data


def test_show_summary_get_with_session(client):
    with client.session_transaction() as session:
        session["club_email"] = clubs[0]["email"]
    response = client.get("/showSummary")
    assert response.status == '200 OK'
    assert b"Welcome" in response.data


def test_display_points(client):
    response = client.get("/display-points")
    assert response.status == '200 OK'
    assert b"Dashboard clubs points" in response.data
    for club in clubs:
        assert bytes(club["name"], "utf-8") in response.data
        assert bytes(str(club["points"]), "utf-8") in response.data


def test_logout(client):
    with client.session_transaction() as session:
        session["club_email"] = clubs[0]["email"]
    response = client.get("/logout")
    assert response.status == '302 Found'  # Redirect to index
    assert b"See the dashboard clubs points" in client.get("/").data
