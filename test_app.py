import unittest
import json
from app import app


class TestFlaskApi(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_post(self):
        response = self.app.post('/set/address?value')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['data']['address']['value'], 'N/A')
        response = self.app.post('/set/name?value=Gideon')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['data']['name']['value'], 'Gideon')

    def test_get(self):
        self.test_post()
        response = self.app.get('/get/name')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['value'], 'Gideon')
        response = self.app.get('/get/address')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['value'], 'N/A')
        response = self.app.get('/get/phone')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 0)

    def test_get_all(self):
        self.test_post()
        response = self.app.get('/get')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['data']), 2)

    def test_clear(self):
        self.test_post()
        response = self.app.get('/clear')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['data']), 0)

    def tearDown(self):
        with open('data.json', 'w') as outfile:
            json.dump({}, outfile)


if __name__ == "__main__":
    unittest.main()
