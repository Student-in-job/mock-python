from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import TIMESTAMP, CHAR, JSONB
from sqlmodel import Field, SQLModel
from datetime import datetime

class Client(SQLModel, table=True):
    __tablename__ = 'clients'
    id: int = Field(
        sa_column=Column(Integer, nullable=False, primary_key=True, name='id')
    )
    client_uuid: str = Field(sa_column=Column(CHAR(9), name='client_uuid'))
    pinfl: str = Field(sa_column=Column(CHAR(14), name='pinfl', index=True))
    status: int = Field(default=1)
    scoring_status: int = Field(default=0)
    is_resident: int = Field(default=1)
    legal_type: int = Field(default=1)
    name: str = Field(max_length=50)
    surname: str = Field(max_length=50)
    patronymic: str = Field(max_length=50, nullable=True)
    gender: int = Field(default=0)
    phone: str = Field(max_length=9)
    birth_date: datetime
    created_at: datetime
    updated_at: datetime = Field(sa_column=Column(TIMESTAMP, default=datetime.now(), name='updated_at'))


class ClientPhone(SQLModel, table=True):
    __tablename__ = 'client_phones'
    id: int = Field(
        sa_column=Column(Integer, nullable=False, primary_key=True, name='id')
    )
    client_id: int | None = Field(default=None, foreign_key="clients.id")
    phone: str = Field(max_length=7, nullable=False)
    is_active: int
    created_at: datetime
    updated_at: datetime = Field(sa_column=Column(TIMESTAMP, default=datetime.now(), name='updated_at'))


class ClientDocument(SQLModel, table=True):
    __tablename__ = 'client_documents'
    id: int = Field(
        sa_column=Column(Integer, nullable=False, primary_key=True, name='id')
    )
    client_id: int | None = Field(default=None, foreign_key="clients.id")
    doc_type_id_cbu: int
    doc_full_name: str = Field(max_length=100)
    pass_data: str = Field(max_length=10)
    issued_date: datetime = Field(nullable=True)
    expiry_date: datetime = Field(nullable=True)
    issued_by: str = Field(max_length=200)
    is_active: int = Field(default=1)
    created_at: datetime
    updated_at: datetime = Field(sa_column=Column(TIMESTAMP, default=datetime.now(), name='updated_at'))


class LegalReportType(SQLModel, table=True):
    __tablename__ = 'client_legal_report_types'
    id: int = Field(
        sa_column=Column(Integer, nullable=False, primary_key=True, name='id')
    )
    code: str = Field(max_length=50, unique=True)
    description: str = Field(max_length=100)
    created_at: datetime
    updated_at: datetime = Field(sa_column=Column(TIMESTAMP, default=datetime.now(), name='updated_at'))


class ClientLegalReport(SQLModel, table=True):
    __tablename__ = 'client_legal_reports'
    id: int = Field(
        sa_column=Column(Integer, nullable=False, primary_key=True, name='id')
    )
    client_id: int | None = Field(default=None, foreign_key="clients.id")
    client_legal_report_type_id: int | None = Field(default=None, foreign_key='client_legal_report_types.id')
    data: dict = Field(sa_type=JSONB)
    created_at: datetime
    updated_at: datetime = Field(sa_column=Column(TIMESTAMP, default=datetime.now(), name='updated_at'))
