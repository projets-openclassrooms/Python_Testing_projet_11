from server import app
from utils import settings

import json
import pytest


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            pass
        yield client


def test_purchase_places(self):
    data = {
        "competition": "Spring Festival",
        "club": "Simply Lift",
        "numberOfPlaces": "25"
    }
    response = self.client.post("/purchasePlaces", data=data)
    assert response.status.code == 200
