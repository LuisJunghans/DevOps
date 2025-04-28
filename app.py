# app.py
from flask import Flask, request, render_template_string

app = Flask(__name__)

def is_valid_password(password):
    if len(password) < 8:
        return False
    has_uppercase = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    return has_uppercase and has_digit

@app.route('/')
def home():
    return '''
    <h1>Validação de Senha</h1>
    <form action="/validate-password" method="post">
        <label for="password">Digite sua senha:</label><br>
        <input type="password" id="password" name="password" required><br><br>
        <button type="submit">Validar</button>
    </form>
    '''

@app.route('/validate-password', methods=['POST'])
def validate_password():
    password = request.form.get('password')
    if is_valid_password(password):
        return render_template_string("<h2>Senha válida! ✅</h2>")
    else:
        return render_template_string("""
            <h2>Senha inválida! ❌</h2>
            <p>Regras: pelo menos 8 caracteres, 1 letra maiúscula e 1 número.</p>
        """)

if __name__ == '__main__':
    app.run(debug=True)
