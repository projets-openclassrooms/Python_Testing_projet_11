from server import app, clubs, competitions, places_to_purchase
from utils import settings

import json
import pytest
from datetime import datetime

from utils.settings import Load_Competitions


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_competition_dates_passees():
    competitions = Load_Competitions()
    for competition in competitions:
        comp_date = datetime.strptime(competition['date'], '%Y-%m-%d %H:%M:%S')
        assert comp_date > datetime(2020, 2, 1), f"La date de la compétition {competition['name']} devrait être postérieure au 1er mars 2020"

