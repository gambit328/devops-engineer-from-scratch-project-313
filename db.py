import os

from sqlmodel import SQLModel, create_engine
from models import Links  # noqa: F401

url = os.getenv("DATABASE_URL")
if url:
    if url.startswith("postgres://"):
        url = "postgresql://" + url[len("postgres://") :]
    engine = create_engine(url)

    SQLModel.metadata.create_all(engine)
