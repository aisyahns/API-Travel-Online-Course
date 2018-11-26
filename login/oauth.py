from flask import Flask, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google

app = Flask(__name__)
app.secret_key = "supersekrit"
blueprint = make_google_blueprint(
    client_id="240737700787-p2ddkfiam3ab541d6s95ol0brbefrd2a.apps.googleusercontent.com",
    client_secret="Nde7D-aUxP4gzVjaXDboNtA4",
    scope=[
        "https://www.googleapis.com/auth/plus.me",
        "https://www.googleapis.com/auth/userinfo.email",
    ]
)
app.register_blueprint(blueprint, url_prefix="/login")

@app.route("/")
def index():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    return "You are {email} on Google".format(email=resp.json()["email"])

if __name__ == "__main__":
    app.run()
