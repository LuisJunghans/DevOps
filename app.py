from flask import Flask, request, render_template_string, redirect, url_for, session, send_from_directory
import json
import os
import string

app = Flask(__name__)
app.secret_key = "admin"
USERS_FILE = 'users.json'

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

def is_valid_password(password):
    if len(password) < 8:
        return False
    has_uppercase = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    #has_special = any(c in string.punctuation for c in password)
    return has_uppercase and has_digit

@app.route('/')
def home():
    return '''
    <h1>Bem-vindo!</h1>
    <p><a href="/register">Registrar-se</a></p>
    <p><a href="/login">Login</a></p>
    '''

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not is_valid_password(password):
            return '''
                <h2>Senha inválida! ❌</h2>
                <p>Regras: 8+ caracteres, 1 letra maiúscula e 1 número.</p>
                <form action="/register">
                    <button type="submit">Voltar ao Cadastro</button>
                </form>
            '''

        users = load_users()
        if username in users:
            return '''
                <h2>Usuário já existe! ❌</h2>
                <form action="/register">
                    <button type="submit">Voltar ao Cadastro</button>
                </form>
            '''

        users[username] = password
        save_users(users)
        return redirect(url_for('login'))

    return '''
    <h1>Registrar</h1>
    <form method="post">
        <label>Usuário:</label><br>
        <input type="text" name="username" required><br>
        <label>Senha:</label><br>
        <input type="password" name="password" required><br><br>
        <button type="submit">Registrar</button>
    </form>
    '''


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        users = load_users()
        if username in users and users[username] == password:
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            return '''
                <h2>Usuário ou senha incorretos! ❌</h2>
                <form action="/login" method="get">
                    <button type="submit">Tentar Novamente</button>
                </form>
            '''

    return '''
    <h1>Login</h1>
    <form method="post">
        <label>Usuário:</label><br>
        <input type="text" name="username" required><br>
        <label>Senha:</label><br>
        <input type="password" name="password" required><br><br>
        <button type="submit">Login</button>
    </form>
    '''

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return send_from_directory('static', 'index.html')
    else:
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)
