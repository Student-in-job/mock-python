import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

import os.path
import models
import routers.clients as clients


@asynccontextmanager
async def init(apps: FastAPI):
    models.create_db_and_tables()
    yield

root_path = os.path.dirname(os.path.realpath(__file__))
application = FastAPI(lifespan=init)
application.mount("/static", StaticFiles(directory=root_path+"/static"), name="static")
application.include_router(clients.router)


@application.get('/favicon.ico', include_in_schema=False, response_class=FileResponse)
async def favicon():
    return root_path + "/static/favicon.ico"


if __name__ == "__main__":
    uvicorn.run(application, host="0.0.0.0", port=8090)