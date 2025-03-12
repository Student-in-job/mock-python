from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

import os.path
import app.models as models
import app.models.test as test
import app.DTO.client as dto_client
import app.classes.my_id_report as my_id

from datetime import datetime

@asynccontextmanager
async def init(apps: FastAPI):
    models.create_db_and_tables()
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
async def get_test_list(session: models.SessionDep):
    statement = models.select(test.Test)
    item = session.exec(statement).first()
    session.close()
    return item

@app.post('/testdb')
async def get_test_list(session: models.SessionDep):
    item = test.Test(id=25, h="Viktor")
    session.add(item)
    session.commit()
    session.close()
    return "Item added"

@app.get('/testdb/list')
async def get_test_list(session: models.SessionDep):
    statement = models.select(test.Test)
    items = session.exec(statement).all()
    session.close()
    return {'items': items}

@app.post('/clients/onboarding')
async def get_test_list(client: dto_client.DTOClient, session: models.SessionDep):
    myid_data: my_id.ReportMYID = client.myIdData
    personal_data: my_id.MyIDProfileCommonData = myid_data.common_data
    doc_data: my_id.MyIDProfileDocData = myid_data.doc_data
    address_data = my_id.MyIDProfileAddress = myid_data.address
    new_client = models.Client(
        client.login,personal_data.pinfl,
        personal_data.first_name,
        personal_data.last_name,
        client.phoneNumber,
        datetime.strptime(personal_data.birth_date, '%d.%m.%Y'), # 22.09.1994
        personal_data.middle_name,
        int(personal_data.gender),
    )
    session.add(new_client)
    session.commit()
    session.refresh(new_client)
    id_client = new_client.id
    new_client_document = models.ClientDocument(
        id_client,
        int(doc_data.doc_type_id_cbu),
        doc_data.doc_type,
        doc_data.pass_data,
        datetime.strptime(doc_data.issued_date, '%d.%m.%Y'),
        datetime.strptime(doc_data.expiry_date,'%d.%m.%Y'),
        doc_data.issued_by_id
    )
    session.add(new_client_document)

    if address_data.permanent_address is not None:
        address_item: my_id.MyIDProfileAddressItem = address_data.permanent_registration
        new_client_address = models.ClientAddress(
            id_client,
            address_item.address,
            address_item.region_id_cbu,
            address_item.district_id_cbu,
            address_item.region_id,
            address_item.district_id
        )
        session.add(new_client_address)
    if address_data.temporary_address is not None:
        address_item: my_id.MyIDProfileAddressItem = address_data.permanent_registration
        new_client_address = models.ClientAddress(
            id_client,
            address_item.address,
            address_item.region_id_cbu,
            address_item.district_id_cbu,
            address_item.region_id,
            address_item.district_id,
            address_type=0
        )
        session.add(new_client_address)

    client_report_myid = models.ClientLegalReport(
        client_id = id_client,
        client_legal_report_type_id=1,
        data=myid_data.model_dump(),
        created_at=datetime.now())
    client_report_katm_universal = models.ClientLegalReport(
        client_id = id_client,
        client_legal_report_type_id=2,
        data=client.katmData,
        created_at=datetime.now())
    session.add(client_report_myid)
    session.add(client_report_katm_universal)
    session.commit()

    session.refresh(new_client)
    session.close()
    return {'client_katm_report': client.katmData}
