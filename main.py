import os

import sentry_sdk
from flask import Flask, redirect, request
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, SQLModel, create_engine, select

from models import Links

app = Flask(__name__)

base_url = os.getenv("BASE_URL")

dsn = os.getenv("SENTRY_DSN")
if dsn:
    sentry_sdk.init(dsn=dsn)

url = os.getenv("DATABASE_URL")
if url:
    if url.startswith("postgres://"):
        url = "postgresql://" + url[len("postgres://") :]
    engine = create_engine(url)

    SQLModel.metadata.create_all(engine)


@app.get("/ping")
def ping():
    return "pong"


@app.get("/raise")
def oops():
    raise RuntimeError("Oops!")


@app.get("/api/links")
def get_links():
    links = []
    with Session(engine) as session:
        statement = select(Links)
        data_from_db = session.exec(statement).all()
        for row in data_from_db:
            link = {
                "id": row.id,
                "original_url": row.original_url,
                "short_name": row.short_name,
                "short_url": f"{base_url}/r/{row.short_name}",
            }
            links.append(link)
    return links


@app.post("/api/links")
def post_links():
    data_user = request.get_json()

    errors = check_request(data_user)
    if errors["detail"]:
        return errors, 422

    link = Links(
        original_url=data_user["original_url"], short_name=data_user["short_name"]
    )

    with Session(engine) as session:
        try:
            session.add(link)
            session.commit()
            session.refresh(link)
        except IntegrityError:
            return {"detail": "short_name already exists"}, 422

        data_added = {
            "id": link.id,
            "original_url": link.original_url,
            "short_name": link.short_name,
            "short_url": f"{base_url}/r/{link.short_name}",
        }

    return data_added, 201


@app.get("/api/links/<int:id>")
def get_link(id):
    with Session(engine) as session:
        found_link = session.get(Links, id)

        if not found_link:
            return {"detail": "A link with this id does not exist"}, 404

        result = {
            "id": found_link.id,
            "original_url": found_link.original_url,
            "short_name": found_link.short_name,
            "short_url": f"{base_url}/r/{found_link.short_name}",
        }

    return result, 200


@app.put("/api/links/<int:id>")
def put_link(id):
    data_user = request.get_json()

    errors = check_request(data_user)
    if errors["detail"]:
        return errors, 422

    with Session(engine) as session:
        found_link = session.get(Links, id)

        if not found_link:
            return {"detail": "The link does not exist"}, 404

        try:
            found_link.original_url = data_user["original_url"]
            found_link.short_name = data_user["short_name"]
            session.commit()
        except IntegrityError:
            return {"detail": "short_name already exists"}, 422

        result = {
            "id": found_link.id,
            "original_url": found_link.original_url,
            "short_name": found_link.short_name,
            "short_url": f"{base_url}/r/{found_link.short_name}",
        }

    return result, 200


@app.delete("/api/links/<int:id>")
def delete_link(id):
    with Session(engine) as session:
        found_link = session.get(Links, id)

        if not found_link:
            return {"detail": "The link does not exist"}, 404

        session.delete(found_link)
        session.commit()

    return "", 204


@app.get("/r/<short_name>")
def get_short_name(short_name):
    with Session(engine) as session:
        stmt = select(Links).where(Links.short_name == short_name)
        found_link = session.exec(stmt).first()

        if not found_link:
            return {"detail": "Link with the short_name does not exist"}, 404

        return redirect(found_link.original_url)


def check_request(data_user):
    result = {"detail": []}

    if type(data_user) is not dict:
        result["detail"].append({"type": "type of data is wrong"})
        return result

    if not "original_url" in data_user:
        result["detail"].append({"original_url": "missing"})
    if not "short_name" in data_user:
        result["detail"].append({"short_name": "missing"})
    return result
