from server import app, clubs, competitions, places_to_purchase
from utils import settings

import json
import pytest

"""
connexion au site
consultation de tableau
inscription un joueur à une future compétition
décompte de points
decompte de places 

"""
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_purchase_places(client):
    data = {
        "club": clubs[0]["name"],
        "numberOfPlaces": "25",
        "competition": competitions[0]["name"],

    }
    response = client.post("/purchasePlaces", data=data)
    assert response.status == '400 BAD REQUEST'


def test_purchase_places_twice(client):
    response = client.get("/book/Fall%20Classic/Simply%20Lift")
    assert response.status == '200 OK'
    # tests à 50% ??


def test_purchase_no_enough_points(client):
    club = clubs[0]
    print(club)
    club['points'] = "0"
    data = {
        "club": club["name"],
        "competition": competitions[0]["name"],
        "numberOfPlaces": "1",

    }
    print(data)
    response = client.post("/purchasePlaces", data=data, follow_redirects=True)
    assert response.status == '400 BAD REQUEST'


def test_purchase_over_12_points(client):
    # should verify if more than 12 points
    club = clubs[1]
    club['points'] = "13"
    print(club)

    data = {
        "club": club["name"],
        "competition": competitions[0]["name"],
        "numberOfPlaces": "13",

    }

    response = client.post("/purchasePlaces", data=data, follow_redirects=True)
    assert response.status == '400 BAD REQUEST'
    assert (b'<!doctype html>\n<html lang=en>\n<title>400 Bad Request</title>\n<h1>Bad Re'
            b'quest</h1>\n<p>The browser (or proxy) sent a request that this server cou'
            b'ld not understand.</p>\n') in response.data


# def test_purchase_under_12_points(client):
#     # should verify if more than 12 points
#     club = clubs[0]
#     print(club)
#     data = {
#         "club": club["name"],
#         "competition": competitions[0]["name"],
#         "numberOfPlaces": "11",
#
#     }
#     response = client.post("/purchasePlaces", data=data, follow_redirects=True)
#     assert response.status == '200 OK'
#     # assert b'Great-booking complete!' in response.data
def test_purchase_places_success(client):
    # Setup
    competitions[0]['numberOfPlaces'] = '10'
    clubs[0]['points'] = '20'
    places_to_purchase.clear()

    # Test
    response = client.post('/purchasePlaces', data={
        'competition': competitions[0]['name'],
        'club': clubs[0]['name'],
        'numberOfPlaces': '5'
    })

    # Assert
    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data
    assert competitions[0]['numberOfPlaces'] == '5'
    assert clubs[0]['points'] == '15'
    assert places_to_purchase[competitions[0]['name']] == 5


def test_purchase_places_no_input(client):
    response = client.post('/purchasePlaces', data={
        'competition': competitions[0]['name'],
        'club': clubs[0]['name'],
        'numberOfPlaces': ''
    })
    assert response.status_code == 400
    assert b"Please enter the right number of places to reserve." in response.data


def test_purchase_places_not_enough_points(client):
    clubs[0]['points'] = '5'
    response = client.post('/purchasePlaces', data={
        'competition': competitions[0]['name'],
        'club': clubs[0]['name'],
        'numberOfPlaces': '10'
    })
    assert b"You don't have enough points." in response.data


def test_purchase_places_not_enough_available(client):
    competitions[0]['numberOfPlaces'] = '5'
    response = client.post('/purchasePlaces', data={
        'competition': competitions[0]['name'],
        'club': clubs[0]['name'],
        'numberOfPlaces': '10'
    })
    assert b"Not enough places available" in response.data


def test_purchase_places_negative_number(client):
    response = client.post('/purchasePlaces', data={
        'competition': competitions[0]['name'],
        'club': clubs[0]['name'],
        'numberOfPlaces': '-5'
    })
    assert b"You can't book a negative number of places." in response.data


def test_purchase_places_more_than_12(client):
    response = client.post('/purchasePlaces', data={
        'competition': competitions[0]['name'],
        'club': clubs[0]['name'],
        'numberOfPlaces': '15'
    })
    assert b"You can't book more than 12 places in a competition." in response.data


def test_purchase_places_exceed_12_total(client):
    places_to_purchase[competitions[0]['name']] = 10
    response = client.post('/purchasePlaces', data={
        'competition': competitions[0]['name'],
        'club': clubs[0]['name'],
        'numberOfPlaces': '5'
    })
    assert b"You can't book more than 12 places for this competition." in response.data


def test_purchase_places_exactly_12_total(client):
    places_to_purchase.clear()
    competitions[0]['numberOfPlaces'] = '20'
    clubs[0]['points'] = '20'
    response = client.post('/purchasePlaces', data={
        'competition': competitions[0]['name'],
        'club': clubs[0]['name'],
        'numberOfPlaces': '12'
    })
    assert b"Great-booking complete!" in response.data
    assert places_to_purchase[competitions[0]['name']] == 12


def test_purchase_places_already_12_booked(client):
    places_to_purchase[competitions[0]['name']] = 12
    response = client.post('/purchasePlaces', data={
        'competition': competitions[0]['name'],
        'club': clubs[0]['name'],
        'numberOfPlaces': '1'
    })
    assert b"You have already booked 12 places for this competition." in response.data

