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


class Guarantor(BaseModel):
    name: str
    phoneNumber: str


class DTOGuarantors(BaseModel):
    guarantors: list[Guarantor]


class DTOReturnClient(BaseModel):
    id: str
    pinfl: str
    status: int
    clientUid: str
    fullName: str
    phoneNumber: str
    scoringStatus: int
    availableLimit: int
    contractAvailability: bool
    hasOverdue: bool
    overdueDays: int
    overdueAmount: int