import os
from functools import wraps

from flask import Flask, redirect, render_template_string, request, session, url_for

app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET", "dev-secret-change-me")

VALID_USER = os.getenv("APP_USER", "testuser")
VALID_PASSWORD = os.getenv("APP_PASSWORD", "testpass")

LOGIN_TEMPLATE = """
<!doctype html>
<html lang=\"it\">
  <head>
    <meta charset=\"utf-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
    <title>Playground ZAP - Login</title>
    <style>
      body { font-family: sans-serif; max-width: 680px; margin: 2rem auto; padding: 0 1rem; }
      input { display: block; margin: .5rem 0 1rem; padding: .4rem; width: 100%; max-width: 320px; }
      button { padding: .5rem .8rem; }
      .error { color: #b00020; }
      .hint { color: #444; font-size: .9rem; }
    </style>
  </head>
  <body>
    <h1>Login Playground</h1>
    {% if error %}<p class=\"error\">{{ error }}</p>{% endif %}
    <form method=\"post\" action=\"{{ url_for('login') }}\">
      <label for=\"username\">Username</label>
      <input id=\"username\" name=\"username\" type=\"text\" required />

      <label for=\"password\">Password</label>
      <input id=\"password\" name=\"password\" type=\"password\" required />

      <button type=\"submit\">Accedi</button>
    </form>
    <p class=\"hint\">Pagina privata: <code>/private</code></p>
  </body>
</html>
"""

HOME_TEMPLATE = """
<!doctype html>
<html lang=\"it\">
  <head>
    <meta charset=\"utf-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
    <title>Playground ZAP</title>
  </head>
  <body>
    <h1>Playground ZAP</h1>
    {% if user %}
      <p>Autenticato come <strong>{{ user }}</strong>.</p>
      <p><a href=\"{{ url_for('private') }}\">Vai alla pagina privata</a></p>
      <p><a href=\"{{ url_for('logout') }}\">Logout</a></p>
    {% else %}
      <p>Utente non autenticato.</p>
      <p><a href=\"{{ url_for('login') }}\">Login</a></p>
    {% endif %}
  </body>
</html>
"""

PRIVATE_TEMPLATE = """
<!doctype html>
<html lang=\"it\">
  <head>
    <meta charset=\"utf-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
    <title>Area Privata</title>
  </head>
  <body>
    <h1>Area privata</h1>
    <p>Contenuto visibile solo dopo login.</p>
    <p><a href=\"{{ url_for('index') }}\">Home</a></p>
  </body>
</html>
"""


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("user"):
            return redirect(url_for("login"))
        return fn(*args, **kwargs)

    return wrapper


@app.get("/")
def index():
    return render_template_string(HOME_TEMPLATE, user=session.get("user"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template_string(LOGIN_TEMPLATE, error=None)

    username = request.form.get("username", "")
    password = request.form.get("password", "")

    if username == VALID_USER and password == VALID_PASSWORD:
        session["user"] = username
        return redirect(url_for("private"))

    return render_template_string(LOGIN_TEMPLATE, error="Credenziali non valide"), 401


@app.get("/private")
@login_required
def private():
    return render_template_string(PRIVATE_TEMPLATE)


@app.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
