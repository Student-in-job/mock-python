from pydantic import BaseModel

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
    status: int = 2
    date: str
    totalAmount: int
    prepaidAmount: int
    paymentsSchedule: list[DTOReturnSchedule]
