import os

import sentry_sdk
from flask import Flask
from sqlmodel import create_engine

app = Flask(__name__)

dsn = os.getenv("SENTRY_DSN")
if dsn:
    sentry_sdk.init(dsn=dsn)

url = os.getenv("DATABASE_URL")
if url:
    if url.startswith("postgres://"):
        url = "postgresql://" + url[len("postgres://") :]
    engine = create_engine(url)


@app.get("/ping")
def ping():
    return "pong"


@app.get("/raise")
def oops():
    raise RuntimeError("Oops!")


@app.get("/api/links")
def get_links():
    pass


@app.post("/api/links")
def post_links():
    pass


@app.get("/api/links/<int:id>")
def get_link(id):
    pass


@app.put("/api/links/<int:id>")
def put_link(id):
    pass


@app.delete("/api/links/<int:id>")
def delete_link(id):
    pass


@app.get("/r/<short_name>")
def get_short_name(short_name):
    pass
