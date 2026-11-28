import os

from flask import Blueprint, redirect, request
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from db import engine
from models import Links

bp = Blueprint("links", __name__)

base_url = os.getenv("BASE_URL")


@bp.get("/api/links")
def get_links():
    links = []

    query_range = request.args.get("range")
    stmt_total = select(func.count()).select_from(Links)
    if query_range is not None:
        range_links = query_range.strip("[]").split(",")
        start = int(range_links[0])
        finish = int(range_links[1])
        stmt = select(Links).order_by(Links.id).limit(finish - start).offset(start)
    else:
        start = None
        finish = None
        stmt = select(Links).order_by(Links.id)

    with Session(engine) as session:
        total = session.exec(stmt_total).one()
        data_from_db = session.exec(stmt).all()
        for row in data_from_db:
            link = serialize_link(row)
            links.append(link)

    if query_range is None:
        return links
    return (links, 200, {"Content-Range": f"links {start}-{finish}/{total}"})


@bp.post("/api/links")
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

        data_added = serialize_link(link)

    return data_added, 201


@bp.get("/api/links/<int:id>")
def get_link(id):
    with Session(engine) as session:
        found_link = session.get(Links, id)

        if not found_link:
            return {"detail": "A link with this id does not exist"}, 404

        result = serialize_link(found_link)

    return result, 200


@bp.put("/api/links/<int:id>")
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

        result = serialize_link(found_link)

    return result, 200


@bp.delete("/api/links/<int:id>")
def delete_link(id):
    with Session(engine) as session:
        found_link = session.get(Links, id)

        if not found_link:
            return {"detail": "The link does not exist"}, 404

        session.delete(found_link)
        session.commit()

    return "", 204


@bp.get("/r/<short_name>")
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


def serialize_link(row):
    link = {
        "id": row.id,
        "original_url": row.original_url,
        "short_name": row.short_name,
        "short_url": f"{base_url}/r/{row.short_name}",
    }
    return link
