import unittest
from server import app


class FlaskIntegrationTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_index(self):
        response = self.client.get('/')
        print("test_index", response)
        self.assertEqual(response.status_code, 200)

    def test_no_email(self):
        response = self.client.get('/showSummary')
        print('test_no_email', response)
        self.assertEqual(response.status_code, 405)

    def test_valid_email(self):
        response = self.client.post('/showSummary', data={'email': "john@simplylift.co"})
        print('test_valid_email', response)
        self.assertEqual(response.status_code, 200)
        assert b'Welcome, john@simplylift.co ' in response.data

    def test_invalid_email(self):
        response = self.client.post('/showSummary', data={'email': "invalid_mail@mail"})
        self.assertEqual(response.status_code, 200)

# texte message erreur


if __name__ == '__main__':
    unittest.main()
