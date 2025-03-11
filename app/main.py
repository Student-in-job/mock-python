from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os.path
import app.models as model
import app.models.test as test
import app.DTO.client as dto_client

@asynccontextmanager
async def init(apps: FastAPI):
    model.create_db_and_tables()
    yield

app = FastAPI(lifespan=init)
root_path = os.path.dirname(os.path.realpath(__file__))


@app.get("/")
async def root():
    return {"message": "Hello World"}

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@app.get("/items2/")
async def read_item2(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

app.mount("/static", StaticFiles(directory=root_path+"/static"), name="static")

@app.get('/favicon.ico', include_in_schema=False, response_class=FileResponse)
async def favicon():
    return root_path + "/static/favicon.ico"

@app.get('/testdb')
async def get_test_list(session: model.SessionDep):
    statement = model.select(test.Test)
    item = session.exec(statement).first()
    session.close()
    return item

@app.post('/testdb')
async def get_test_list(session: model.SessionDep):
    item = test.Test(id=25, h="Viktor")
    session.add(item)
    session.commit()
    session.close()
    return "Item added"

@app.get('/testdb/list')
async def get_test_list(session: model.SessionDep):
    statement = model.select(test.Test)
    items = session.exec(statement).all()
    session.close()
    return {'items': items}

@app.post('/clients/onboarding')
async def get_test_list(client: dto_client.DTOClient):
    results = client
    return {'client': results}
