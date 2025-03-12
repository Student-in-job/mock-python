from app.classes.my_id_report import ReportMYID
from pydantic import BaseModel


class DTOClient(BaseModel):
    pinfl: str
    login: str
    phoneNumber: str
    photoUrl: str
    myIdData: ReportMYID | None
    katmData: dict | None = None
    gnkData: dict | None = None