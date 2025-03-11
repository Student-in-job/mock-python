from typing import Annotated
from datetime import datetime
from fastapi import Depends
from sqlmodel import Session, create_engine, SQLModel, select

import app.models.client as client_models
import app.models.partner as partner_models
import app.models.contract as contract_models
import app.models.limit as limit_models

from app.models.migrations import init_limit_types, init_clients, init_partners
from app.models.app_settings import AppSettings
from app.settings import Settings


settings = Settings()
engine = create_engine(settings.DATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


def create_db_and_tables():
    SQLModel.metadata.drop_all(engine, checkfirst=True)
    SQLModel.metadata.create_all(engine, checkfirst=True)
    init_limit_types(engine)
    init_clients(engine)
    init_partners(engine)
    # p = save_contract(Session(engine))


def save_contract(session: Session):
    item = contract_models.Contract(
        client_id=12,
        total_amount=100000,
        profit_amount=44000,
        period=12,
        tariff_plan_id=1,
        partner_id=1,
        created_at=datetime.now())
    session.add(item)
    session.commit()
    session.close()
    return "Item added"


