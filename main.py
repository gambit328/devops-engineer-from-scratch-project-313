from flask import Flask
import os, sentry_sdk

app = Flask(__name__)

dsn = os.getenv("SENTRY_DSN")
if dsn:
    sentry_sdk.init(dsn=dsn)


@app.get("/ping")
def ping():
    return "pong"
