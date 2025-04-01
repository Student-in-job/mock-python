from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import TIMESTAMP, CHAR
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime


class CardOperations(SQLModel, table=True):
    __tablename__ = 'operations_card'
    id: int = Field(
        sa_column=Column(Integer, nullable=False, primary_key=True, name='id')
    )
    client_id: int | None = Field(default=None, foreign_key="clients.id", ondelete='CASCADE')
    phone: str = Field(sa_column=Column(CHAR(16), name='phone'))
    pan: str = Field(sa_column=Column(CHAR(16), name='pan'))
    expire: str = Field(sa_column=Column(CHAR(4), name='expire'))
    operation_id: str
    otp_code: str = Field(sa_column=Column(CHAR(6), name='otp_code'))
    is_confirmed: int = Field(default=0)
    created_at: datetime
    updated_at: datetime = Field(sa_column=Column(TIMESTAMP, default=datetime.now(), name='updated_at'))

    def __init__(self, client_id: int, phone: str, pan: str, expire: str, operation_id: str,
                 otp_code: str, is_confirmed: int = None):
        super().__init__()
        self.client_id = client_id
        self.phone = phone
        self.pan = pan
        self.expire = expire
        self.operation_id = operation_id
        self.otp_code = otp_code
        self.is_confirmed = is_confirmed
        self.created_at = datetime.now()


class Card(SQLModel, table=True):
    __tablename__ = 'cards'
    id: int = Field(
        sa_column=Column(Integer, nullable=False, primary_key=True, name='id')
    )
    client_id: int | None = Field(default=None, foreign_key="clients.id", ondelete='CASCADE')
    phone: str = Field(sa_column=Column(CHAR(16), name='phone'))
    pan: str = Field(sa_column=Column(CHAR(16), name='pan'))
    expire: str = Field(sa_column=Column(CHAR(4), name='expire'))
    created_at: datetime
    updated_at: datetime = Field(sa_column=Column(TIMESTAMP, default=datetime.now(), name='updated_at'))

    def __init__(self, client_id: int, phone: str, pan: str, expire: str):
        super().__init__()
        self.client_id = client_id
        self.phone = phone
        self.pan = pan
        self.expire = expire
        self.created_at = datetime.now()
