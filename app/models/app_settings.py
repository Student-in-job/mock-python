from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import TIMESTAMP, JSONB
import uuid as uuid_pkg
from sqlmodel import Field, SQLModel
from datetime import datetime

class AppSettings(SQLModel, table=True):
    __tablename__ = 'application_settings'
    id: int = Field(
        sa_column=Column(Integer, nullable=False, primary_key=True, name='id')
    )