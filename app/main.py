from contextlib import asynccontextmanager
from fastapi import FastAPI, Response, status, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

import os.path
import app.models as models
import app.models.test as test
from app.DTO import DTOScore, DTOClient
import app.classes.my_id_report as my_id

from datetime import datetime


@asynccontextmanager
async def init(apps: FastAPI):
    models.create_db_and_tables()
    yield

app = FastAPI(lifespan=init)
root_path = os.path.dirname(os.path.realpath(__file__))
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
async def client_set_client(client: DTOClient, session: models.SessionDep):
    myid_data: my_id.ReportMYID = client.myIdData
    personal_data: my_id.MyIDProfileCommonData = myid_data.common_data
    doc_data: my_id.MyIDProfileDocData = myid_data.doc_data
    address_data = my_id.MyIDProfileAddress = myid_data.address
    new_client = models.Client(
        client.login,
        personal_data.pinfl,
        personal_data.first_name,
        personal_data.last_name,
        client.phoneNumber,
        datetime.strptime(personal_data.birth_date, '%d.%m.%Y'),  # 22.09.1994
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
        datetime.strptime(doc_data.expiry_date, '%d.%m.%Y'),
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
        client_id=id_client,
        client_legal_report_type_id=1,
        data=myid_data.model_dump(),
        created_at=datetime.now())
    client_report_katm_universal = models.ClientLegalReport(
        client_id=id_client,
        client_legal_report_type_id=2,
        data=client.katmData,
        created_at=datetime.now())
    session.add(client_report_myid)
    session.add(client_report_katm_universal)
    session.commit()

    session.refresh(new_client)
    session.close()
    return {'client_katm_report': client.katmData}


@app.post('/clients/give-limit')
async def client_set_score(score: DTOScore, session: models.SessionDep, response: Response):
    session.statement = models.select(models.Client).where(models.Client.id == score.client_id)
    results = session.exec(session.statement)
    found: bool = False
    if len(results.fetchall()) > 0:
        new_limit_transaction: models.LimitBalanceTransaction = models.LimitBalanceTransaction(
            score.client_id,
            score.limit_value,
            models.LimitTransactionTypes.SCORE
        )
        session.statement = models.select(models.LimitBalance).where(models.LimitBalance.client_id == score.client_id)
        results = session.exec(session.statement)
        new_limit_balance = results.first()
        if new_limit_balance is None:
            new_limit_balance = models.LimitBalance(score.client_id, score.limit_value)
        else:
            new_limit_balance.value += score.limit_value
        session.add(new_limit_transaction)
        session.add(new_limit_balance)
        session.commit()
        found = True
    session.close()
    if not found:
        response.status_code = status.HTTP_400_BAD_REQUEST
        result_message = 'Error ca\'t find client'
    else:
        result_message = 'Created'
    return result_message


@app.get('/clients/by-pinfl')
async def client_get_client(session: models.SessionDep, response: Response, pinfl: str = Query(max_length=14)):
    session.statement = models.select(models.Client).where(models.Client.pinfl == pinfl)
    results = session.exec(session.statement)
    client = results.first()
    return client
