from pydantic import BaseModel


class DTOCard(BaseModel):
    phoneNumber: str
    pan: str
    expiry: int


class DTOCardConfirmation(BaseModel):
    operationId: str
    otp: str
