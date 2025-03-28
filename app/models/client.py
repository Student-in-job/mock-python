from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import TIMESTAMP, CHAR, JSONB
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime

class Client(SQLModel, table=True):
    __tablename__ = 'clients'
    id: int = Field(
        sa_column=Column(Integer, nullable=False, primary_key=True, name='id')
    )
    client_uuid: str = Field(sa_column=Column(CHAR(9), name='client_uuid'))
    pinfl: str = Field(sa_column=Column(CHAR(14), name='pinfl', index=True))
    status: int = Field(default=2)
    scoring_status: int = Field(default=0)
    is_resident: int = Field(default=1)
    legal_type: int = Field(default=1)
    name: str = Field(max_length=50)
    surname: str = Field(max_length=50)
    patronymic: str = Field(max_length=50, nullable=True)
    gender: int = Field(default=0)
    phone: str = Field(max_length=12)
    birth_date: datetime
    created_at: datetime
    updated_at: datetime = Field(sa_column=Column(TIMESTAMP, default=datetime.now(), name='updated_at'))
    # phones: list["ClientPhone"] = Relationship(back_populates='client')
    documents: list["ClientDocument"] = Relationship(back_populates='client')
    addresses: list["ClientAddress"] = Relationship(back_populates='client')
    has_overdue: int = Field(default=0)
    overdue_days: int = Field(default=-1)
    overdue_amount: int = Field(default=0)

    def __init__(self, client_uuid: str, pinfl: str, name: str, surname: str, phone: str,
                 birth_date: datetime, patronymic: str=None, gender: int=None):
        super().__init__()
        self.client_uuid = client_uuid
        self.pinfl = pinfl
        self.name = name
        self.surname = surname
        self.phone = phone
        self.birth_date = birth_date
        self.patronymic = patronymic
        self.gender = gender
        self.created_at = datetime.now()


# class ClientPhone(SQLModel, table=True):
#     __tablename__ = 'client_phones'
#     id: int = Field(
#         sa_column=Column(Integer, nullable=False, primary_key=True, name='id')
#     )
#     client_id: int | None = Field(default=None, foreign_key="clients.id", ondelete='CASCADE')
#     phone: str = Field(max_length=7, nullable=False)
#     is_active: int
#     created_at: datetime
#     updated_at: datetime = Field(sa_column=Column(TIMESTAMP, default=datetime.now(), name='updated_at'))
#     client: Client = Relationship(back_populates='phones')


class ClientDocument(SQLModel, table=True):
    __tablename__ = 'client_documents'
    id: int = Field(
        sa_column=Column(Integer, nullable=False, primary_key=True, name='id')
    )
    client_id: int | None = Field(default=None, foreign_key="clients.id", ondelete='CASCADE')
    doc_type_id_cbu: int
    doc_full_name: str = Field(max_length=100)
    pass_data: str = Field(max_length=10)
    issued_date: datetime = Field(nullable=True)
    expiry_date: datetime = Field(nullable=True)
    issued_by: str = Field(max_length=200)
    is_active: int = Field(default=1)
    created_at: datetime
    updated_at: datetime = Field(sa_column=Column(TIMESTAMP, default=datetime.now(), name='updated_at'))
    client: Client = Relationship(back_populates='documents')

    def __init__(self, client_id: int, doc_type_id_cbu: int, doc_full_name: str, pass_data: str, issued_date: datetime,
                 expiry_date: datetime, issued_by: str, is_active: int=1):
        super().__init__()
        self.client_id = client_id
        self.doc_type_id_cbu = doc_type_id_cbu
        self.doc_full_name = doc_full_name
        self.pass_data = pass_data
        self.issued_date = issued_date
        self.expiry_date = expiry_date
        self.issued_by = issued_by
        self.created_at = datetime.now()

class ClientAddress(SQLModel, table = True):
    __tablename__ = 'client_addresses'
    id: int = Field(
        sa_column=Column(Integer, nullable=False, primary_key=True, name='id')
    )
    client_id: int | None = Field(default=None, foreign_key="clients.id", ondelete='CASCADE')
    region_id_cbu: int = Field(nullable=True)
    district_id_cbu: int = Field(nullable=True)
    region_id_myid: int = Field(nullable=True)
    district_id_myid: int = Field(nullable=True)
    address: str = Field(max_length=300)
    address_type: int
    is_active: int = Field(default=1)
    created_at: datetime
    updated_at: datetime = Field(sa_column=Column(TIMESTAMP, default=datetime.now(), name='updated_at'))
    client: Client = Relationship(back_populates='addresses')

    def __init__(self, client_id: int, address:str, region_id_cbu:int=None, district_id_cbu:int=None,
                 region_id_myid: int=None, district_id_myid: int=None, is_active: int=None, address_type: int = 1):
        super().__init__()
        self.client_id = client_id
        self.address = address
        self.region_id_cbu = region_id_cbu
        self.district_id_cbu = district_id_cbu
        self.region_id_myid = region_id_myid
        self.district_id_myid = district_id_myid
        self.is_active = is_active
        self.address_type = address_type
        self.created_at = datetime.now()


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


class ClientGuarantor(SQLModel, table=True):
    __tablename__ = 'client_guarantors'
    id: int = Field(
        sa_column=Column(Integer, nullable=False, primary_key=True, name='id')
    )
    client_id: int = Field(default=None, foreign_key="clients.id", ondelete='CASCADE')
    name: str = Field(max_length=150)
    phone: str = Field(sa_column=Column(CHAR(12), name='phone', index=True))
    created_at: datetime
    updated_at: datetime = Field(sa_column=Column(TIMESTAMP, default=datetime.now(), name='updated_at'))

    def __init__(self, client_id: int, name: str, phone: str):
        super().__init__()
        self.client_id = client_id
        self.name = name
        self.phone = phone
        self.created_at = datetime.now()
        