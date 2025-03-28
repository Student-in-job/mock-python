from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import TIMESTAMP, JSONB
import uuid as uuid_pkg
from sqlmodel import Field, SQLModel
from datetime import datetime


class Contract(SQLModel, table=True):
    __tablename__ = 'contracts'
    id: int = Field(
        sa_column=Column(Integer, nullable=False, primary_key=True, name='id')
    )
    uuid: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4,
        nullable=False
    )
    contract_uid: str = Field(max_length=50, nullable=True)
    client_id: int = Field(foreign_key='clients.id')
    total_amount: int
    profit_amount: int
    period: int
    activated_at: datetime = Field(nullable=True)
    tariff_plan_id: int = Field(foreign_key='tariff_plans.id')
    closed_at: datetime = Field(nullable=True)
    closed_reason: int = Field(default=0, index=True)
    activation_status: int = Field(default=0, index=True)
    status: int = Field(default=0, index=True)
    partner_id: int = Field(foreign_key='partners.id')
    extra_debt_amount: int = Field(default=0)
    is_full_debt_required: int = Field(default=0, index=True)
    date_of_full_debt_required: datetime = Field(nullable=True)
    overdue_days: int = Field(default=-1)
    overdue_amount: int = Field(default=0)
    created_at: datetime
    updated_at: datetime = Field(sa_column=Column(TIMESTAMP, default=datetime.now(), name='updated_at'))

    def __init__(self, client_id: int, total_amount: int, profit_amount: int, period: int, tariff_plan_id: int,
                 partner_id: int):
        super().__init__()
        self.client_id = client_id
        self.total_amount = total_amount
        self.profit_amount = profit_amount
        self.period = period
        self.tariff_plan_id = tariff_plan_id
        self.partner_id = partner_id
        self.created_at = datetime.now()


class ContractMerchant(SQLModel, table=True):
    __tablename__ = 'contract_merchants'
    id: int = Field(
        sa_column=Column(Integer, nullable=False, primary_key=True, name='id')
    )
    inn: str = Field(max_length=14)
    brand_name: str = Field(max_length=100)
    legal_name: str = Field(max_length=100)
    contract_id: int = Field(foreign_key='contracts.id')
    created_at: datetime
    updated_at: datetime = Field(sa_column=Column(TIMESTAMP, default=datetime.now(), name='updated_at'))

    def __init__(self, inn: str, brand_name: str, legal_name: str, contract_id: int):
        super().__init__()
        self.inn = inn
        self.brand_name = brand_name
        self.legal_name = legal_name
        self.contract_id = contract_id
        self.created_at = datetime.now()


class ContractSchedule(SQLModel, table=True):
    __tablename__ = 'contract_schedules'
    id: int = Field(
        sa_column=Column(Integer, nullable=False, primary_key=True, name='id')
    )
    contract_id: int = Field(foreign_key='contracts.id')
    amount: int = Field(default=0)
    profit_amount: int = Field(default=0)
    paid_amount: int = Field(default=0)
    payment_date: datetime = Field(nullable=True)
    full_paid_at: datetime = Field(nullable=True)
    status: int = Field(default=0)
    schedule_type: int = Field(default=0)
    created_at: datetime
    updated_at: datetime = Field(sa_column=Column(TIMESTAMP, default=datetime.now(), name='updated_at'))

    def __init__(self, contract_id: int, amount: int, profit_amount: int, payment_date: datetime = None,
                 schedule_type: int = None):
        super().__init__()
        self.contract_id = contract_id
        self.amount = amount
        self.profit_amount = profit_amount
        self.payment_date = payment_date
        self.schedule_type = schedule_type
        self.created_at = datetime.now()


class ContractMyIdReport(SQLModel, table=True):
    __tablename__ = 'contract_myid_reports'
    id: int = Field(
        sa_column=Column(Integer, nullable=False, primary_key=True, name='id')
    )
    contract_id: int = Field(foreign_key='contracts.id')
    data: dict = Field(sa_type=JSONB, nullable=True)
    created_at: datetime
    updated_at: datetime = Field(sa_column=Column(TIMESTAMP, default=datetime.now(), name='updated_at'))
