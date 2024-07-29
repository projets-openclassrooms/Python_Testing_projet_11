from server import app, clubs, competitions
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
