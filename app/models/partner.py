from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import TIMESTAMP, CHAR
from sqlmodel import Field, SQLModel
from datetime import datetime


class Partner(SQLModel, table=True):
    __tablename__ = 'partners'
    id: int = Field(
        sa_column=Column(Integer, nullable=False, primary_key=True, name='id')
    )
    name: str = Field(max_length=100)
    inn: str = Field(max_length=14)
    address: str = Field(max_length=100, nullable=True)
    legal_address: str = Field(max_length=100, nullable=True)
    mfo: str = Field(sa_column=Column(CHAR(5), name='mfo', index=True))
    bank_name: str = Field(max_length=100, nullable=True)
    bank_account: str = Field(sa_column=Column(CHAR(20), name='bank_account', index=True))
    vat_number: str = Field(sa_column=Column(CHAR(12), name='vat_number', index=True))
    oked: str = Field(sa_column=Column(CHAR(5), name='oked', index=True))
    description: str = Field(max_length=100, nullable=True)
    status: int = Field(default=1)
    access_token: str = Field(max_length=100)
    created_at: datetime
    updated_at: datetime = Field(sa_column=Column(TIMESTAMP, default=datetime.now(), name='updated_at'))


class TariffPlan(SQLModel, table=True):
    __tablename__ = 'tariff_plans'
    id: int = Field(
        sa_column=Column(Integer, nullable=False, primary_key=True, name='id')
    )
    name: str = Field(max_length=50)
    period: int
    markup_rate: int = Field(default=0)
    markup_type: int = Field(default=1)
    is_grace_available: int = Field(default=0)
    discount_rate: int = Field(default=0)
    is_active: int = Field(default=1)
    created_at: datetime
    updated_at: datetime = Field(sa_column=Column(TIMESTAMP, default=datetime.now(), name='updated_at'))


class PartnerTariffPlan(SQLModel, table=True):
    __tablename__ = 'partner_tariff_plan'
    id: int = Field(
        sa_column=Column(Integer, nullable=False, primary_key=True, name='id')
    )
    partner_id: int = Field(foreign_key='partners.id')
    tariff_plan_id: int = Field(foreign_key='tariff_plans.id')
    activate_at: datetime = Field(sa_column=Column(TIMESTAMP, default=datetime.now(), name='activate_at'))
    created_at: datetime
    updated_at: datetime = Field(sa_column=Column(TIMESTAMP, default=datetime.now(), name='updated_at'))


