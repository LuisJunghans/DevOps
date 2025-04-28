import unittest
from app import app

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        # Configura o app para teste
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'test_secret'
        self.app = app.test_client()

    def test_register_page_loads(self):
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registrar', response.data)

    def test_login_page_loads(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_login_invalid(self):
        response = self.app.post('/login', data=dict(
            username="fakeuser",
            password="fakepass"
        ), follow_redirects=True)
        self.assertIn(b'Usu\xc3\xa1rio ou senha incorretos', response.data)

if __name__ == '__main__':
    unittest.main()
