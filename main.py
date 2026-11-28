import os

import sentry_sdk
from flask import Flask, send_from_directory

from routes import bp

app = Flask(__name__, static_folder="public", static_url_path="")
app.register_blueprint(bp)


dsn = os.getenv("SENTRY_DSN")
if dsn:
    sentry_sdk.init(dsn=dsn)


@app.get("/ping")
def ping():
    return "pong"


@app.get("/raise")
def oops():
    raise RuntimeError("Oops!")


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Expose-Headers"] = "Content-Range"
    return response


@app.get("/")
def index():
    return send_from_directory("public", "index.html")
