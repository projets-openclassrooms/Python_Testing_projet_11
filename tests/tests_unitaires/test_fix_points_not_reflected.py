import pytest

from server import app, clubs, competitions, places_to_purchase


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_purchase_places(client):
    # Réinitialiser les données avant le test
    # clubs[0]["points"] = "30"
    # competitions[0]["numberOfPlaces"] = "25"
    # places_to_purchase.clear()

    initial_club_points = int(clubs[0]["points"])
    initial_competition_places = int(competitions[0]["numberOfPlaces"])

    response = client.post(
        "/purchasePlaces",
        data={"club": clubs[0]["name"], "competition": competitions[0]["name"], "places": "1"},
        follow_redirects=True,
    )

    assert response.status == '200 OK'
    assert b"Great-booking complete!" in response.data
    assert int(clubs[0]["points"]) == initial_club_points - 1
    assert int(competitions[0]["numberOfPlaces"]) == initial_competition_places - 1


# def test_purchase_places_not_enough_points(client):
#     # Réinitialiser les données avant le test
#     clubs[0]["points"] = 0
#     competitions[0]["numberOfPlaces"] = "25"
#     places_to_purchase.clear()
#
#     response = client.post(
#         "/purchasePlaces",
#         data={"club": clubs[0]["name"], "competition": competitions[0]["name"], "places": "25"},
#         follow_redirects=True,
#     )
#
#     assert response.status == '200 OK'
#     assert b"You don't have enough points." in response.data
#     assert clubs[0]["points"] == 0
