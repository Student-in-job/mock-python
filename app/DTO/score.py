from pydantic import BaseModel


class DTOScore(BaseModel):
    client_id: int
    limit_value: int