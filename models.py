from datetime import datetime

from sqlmodel import Field, SQLModel


class Links(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    original_url: str
    short_name: str = Field(unique=True)
    created_at: datetime = Field(default_factory=datetime.now)
