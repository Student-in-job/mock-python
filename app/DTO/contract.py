from pydantic import BaseModel
from typing import Union
from classes.my_id_report import ReportMYID


class DTOMerchant(BaseModel):
    inn: str
    brandName: str
    legalName: str


class DTOContract(BaseModel):
    clientId: str
    partnerId: str
    tariffPlanId: int
    amount: int
    merchant: DTOMerchant


class DTOReturnSchedule (BaseModel):
    paymentDate: str
    amount: int


class DTOReturnContract(BaseModel):
    operationId: str
    duration: int
    status: int
    date: str
    totalAmount: int
    prepaidAmount: int
    paymentsSchedule: Union[list[BaseModel], list]


class DTOContractConfirm(BaseModel):
    operationId: str
    myIdData: ReportMYID = None
    photoURL: str = None


class DTOReturnScheduleInfo(BaseModel):
    paymentDate: str
    amount: int
    paidAmount: int
    status: int


class DTOReturnContractInfo(BaseModel):
    id: str
    actUrl: str
    duration: int
    status: int
    date: str
    totalAmount: int
    originAmount: int
    overdueDays: int
    overdueAmount: int
    prepaidAmount: int
    merchant: DTOMerchant = None
    paymentsSchedule: Union[list[BaseModel], list]
