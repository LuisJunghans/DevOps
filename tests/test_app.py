import sys
import os
import time
import unittest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app

class FlaskTestCase(unittest.TestCase):
    # Configura o app para teste
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'test_secret'
        self.app = app.test_client()

         # Limpa o arquivo de usuários antes de cada teste
    with open('users.json', 'w') as f:
        f.write('{}')

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

    def test_register_with_special_char_password(self):
        unique_username = f"usuarioTeste{int(time.time())}"
        response = self.app.post('/register', data=dict(
            username=unique_username,
            password="Senha123!",
        ), follow_redirects=True)
        self.assertIn(b'Login', response.data)


if __name__ == '__main__':
    unittest.main()
