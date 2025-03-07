from typing import Annotated
from datetime import datetime
from fastapi import Depends

import app.models.client
import app.models.contract
from sqlmodel import Session, create_engine, select, SQLModel
from app.settings import Settings

settings = Settings()
engine = create_engine(settings.DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


def create_db_and_tables():
    # event.listen(
    #     SQLModel.metadata,
    #     "before_create",
    #     DDL(
    #         "DROP TABLE IF EXISTS hero"
    #     )
    # )
    SQLModel.metadata.create_all(engine, checkfirst=True)
    # p = save_client(Session(engine))

def save_client(session: SessionDep):
    item = contract.Contracts(
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