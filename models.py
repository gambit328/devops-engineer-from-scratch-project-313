from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


class Links(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    original_url: str
    short_name: str = Field(unique=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
