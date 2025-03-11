from pydantic import BaseModel


class DTOClient(BaseModel):
    pinfl: str
    login: str
    phoneNumber: str
    photoUrl: str
    myIdData: dict | None
    katmData: dict | None = None
    gnkData: dict | None = None