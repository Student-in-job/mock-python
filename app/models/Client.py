from typing import Annotated

from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, Session, SQLModel, create_engine, select

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: str
    data: dict = Field(sa_type=JSONB, nullable=True)

class test(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    h: str