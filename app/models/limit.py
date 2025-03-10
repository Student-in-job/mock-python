from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import TIMESTAMP, CHAR
from sqlmodel import Field, SQLModel
from datetime import datetime


class LimitBalance(SQLModel, table=True):
    __tablename__ = 'limit_balances'
    id: int = Field(
        sa_column=Column(Integer, nullable=False, primary_key=True, name='id')
    )
    client_id: int | None = Field(default=None, foreign_key="clients.id")
    value: int = Field(default=0)
    created_at: datetime
    updated_at: datetime = Field(sa_column=Column(TIMESTAMP, default=datetime.now(), name='updated_at'))


class LimitTransactionType(SQLModel, table=True):
    __tablename__ = 'limit_balance_transaction_types'
    id: int = Field(primary_key=True)
    code: str = Field(max_length=50)
    description: str = Field(max_length=100)
    created_at: datetime
    updated_at: datetime = Field(sa_column=Column(TIMESTAMP, default=datetime.now(), name='updated_at'))


class LimitBalanceTransaction(SQLModel, table=True):
    __tablename__ = 'limit_balance_transactions'
    id: int = Field(
        sa_column=Column(Integer, nullable=False, primary_key=True, name='id')
    )
    client_id: int | None = Field(default=None, foreign_key='clients.id')
    contract_id: int = Field(nullable=True, foreign_key='contracts.id')
    amount: int = Field(default=0)
    limit_balance_transaction_type_id: int = Field(foreign_key='limit_balance_transaction_types.id')
    created_at: datetime
    updated_at: datetime = Field(sa_column=Column(TIMESTAMP, default=datetime.now(), name='updated_at'))
