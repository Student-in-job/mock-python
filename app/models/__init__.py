from sqlalchemy import event, DDL

import app.models.Client
from sqlmodel import Session, create_engine, select, SQLModel

database_url = f"postgresql+psycopg2://mock_python_user:jw8s0F4@localhost:5432/mock_integration_test"
engine = create_engine(database_url)


def test_item():
    with Session(engine) as session:
        statement = select(Client.test)
        item = session.exec(statement).first()
        session.close()
    return item

def test_add():
    item = Client.test( id=23, h="Vitaliy")
    with Session(engine) as session:
        session.add(item)
        session.commit()
        session.close()
    return "Item added"

def test_list():
    with Session(engine) as session:
        statement = select(Client.test)
        items = session.exec(statement).all()
        session.close()
    return items

def create_db_and_tables():
    # event.listen(
    #     SQLModel.metadata,
    #     "before_create",
    #     DDL(
    #         "DROP TABLE hero"
    #     )
    # )
    SQLModel.metadata.create_all(engine, checkfirst=True)

def get_session():
    with Session(engine) as session:
        yield session