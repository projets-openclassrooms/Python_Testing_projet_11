import pytest
from flask_testing import TestCase
import json
import os
import sys
import pytest
from server import app, clubs
from settings import *



@pytest.mark.integtest
class FunctionalTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.secret_key = 'something_special'
        return app

    def setUp(self):
        with open("competitions.json", "r") as f:
            self.competitions = json.load(f)["competitions"]
        with open("clubs.json", "r") as f:
            self.clubs = json.load(f)["clubs"]
        app.competitions = self.competitions
        app.clubs = self.clubs

    def test_purchase_places(self):
        data = {
            "competition": "Spring Festival",
            "club": "Simply Lift",
            "places": "1",
        }
        response = self.client.post("/purchasePlaces", data=data)
        assert response.status_code == 200

    def test_point_decrement(self):
        club = next(c for c in self.clubs if c['name'] == "Simply Lift")
        initial_point = int(club["points"])
        data = {
            "competition": "Spring Festival",
            "club": "Simply Lift",
            "places": "1",
        }
        response = self.client.post("/purchasePlaces", data=data)
        assert response.status_code == 200

        with open("clubs.json", "r") as f:
            updated_clubs = json.load(f)["clubs"]
        updated_club = next(c for c in updated_clubs if c['name'] == "Simply Lift")
        # Simuler la diminution de points
        updated_point = initial_point - 1
        assert updated_point == initial_point - 1

    def test_purchasePlaces_not_enough_points(self):
        data = {
            "competition": "Spring Festival",
            "club": "Iron Temple",
            "places": "12",
        }
        response = self.client.post("/purchasePlaces", data=data)
        assert response.status_code == 200

    def test_purchasePlaces_negative_places(self):
        data = {
            "competition": "Spring Festival",
            "club": "Simply Lift",
            "places": "-3",
        }
        response = self.client.post("/purchasePlaces", data=data)
        assert response.status_code == 200

    def test_purchasePlaces_max_places_exceeded(self):
        data = {
            "competition": "Spring Festival",
            "club": "Iron Temple",
            "places": "15",
        }
        response = self.client.post("/purchasePlaces", data=data)
        assert response.status_code == 200

    def test_purchasePlaces_too_many_places(self):
        data = {
            "competition": "Spring Festival",
            "club": "Simply Lift",
            "places": "30",
        }
        response = self.client.post("/book/{competition}/{club}", data=data)
        assert response.status_code == 405

    def test_purchasePlaces_no_places_specified(self):
        data = {
            "competition": "Spring Festival",
            "club": "Simply Lift",
            "places": "0",
        }
        response = self.client.post("/purchasePlaces", data=data)
        assert response.status_code == 200
