# tests/test_api.py
import unittest
from old import create_app
from flask.testing import FlaskClient

class TestAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()
        cls.app.testing = True

    def test_generate_session(self):
        response = self.client.post('/api/generate_session', json={
            'themes': ['empty', 'submission'],
            'duration': 15,
            'difficulty': 'MODERATE',
            'dominant_name': 'Master',
            'subject_name': 'Slave',
            'sub_pov': '1PS',
            'dom_pov': '2PS'
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('session_id', data)
        self.assertIn('phases', data)
        self.assertGreater(len(data['phases']), 0)

    def test_invalid_endpoint(self):
        response = self.client.get('/api/non_existent_endpoint')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
