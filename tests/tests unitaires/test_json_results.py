from server import app, clubs, competitions, places_to_purchase
from utils import settings

import json
import pytest


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


