import unittest
from administradores import app

class TestAdministradores(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_get_administradores(self):
        response = self.client.get("/administradores")
        self.assertEqual(response.status_code, 200)
        self.assertIn("João Carlos", response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()