import os

import sentry_sdk
from flask import Flask
from sqlmodel import create_engine

app = Flask(__name__)

dsn = os.getenv("SENTRY_DSN")
if dsn:
    sentry_sdk.init(dsn=dsn)

url = os.getenv("DATABASE_URL")
if url and url.startswith("postgres://"):
    url = "postgresql://" + url[len("postgres://") :]
engine = create_engine(url)


@app.get("/ping")
def ping():
    return "pong"


@app.get("/raise")
def oops():
    raise RuntimeError("Oops!")
