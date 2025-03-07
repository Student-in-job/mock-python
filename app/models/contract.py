from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP
import uuid as uuid_pkg
from sqlmodel import Field, SQLModel
from datetime import datetime

class Contracts(SQLModel, table=True):
    id: int = Field(
        sa_column=Column(Integer, nullable=False, primary_key=True, name='id')
    )
    uuid: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4,
        nullable=False
    )
    contract_uid: str = Field(max_length=50, nullable=True)
    client_id: int
    total_amount: int
    profit_amount: int
    period: int
    activated_at: datetime = Field(nullable=True)
    tariff_plan_id: int
    closed_at: datetime = Field(nullable=True)
    closed_reason: int = Field(default=0, index=True)
    activation_status: int = Field(default=0, index=True)
    status: int = Field(default=0, index=True)
    partner_id: int
    extra_debt_amount: int = Field(default=0)
    is_full_debt_required: int = Field(default=0, index=True)
    date_of_full_debt_required: datetime = Field(nullable=True)
    created_at: datetime
    updated_at: datetime = Field(sa_column=Column(TIMESTAMP, default=datetime.now(), name='updated_at'))