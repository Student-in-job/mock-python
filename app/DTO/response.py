from pydantic import BaseModel
from typing import Any, Union


class DTOErrorData(BaseModel):
    error_code: int = None

    def __init__(self, code: int):
        super().__init__()
        self.error_code = code


class DTOError(BaseModel):
    error: bool = True
    message: str = ''
    data: DTOErrorData = None

    def __init__(self, code: int, message: str):
        super().__init__()
        self.data = DTOErrorData(code)
        self.message = message


class DTOResponse(BaseModel):
    error: bool = False
    message: str = ''
    data: Any = None

    def __init__(self, message: str, data: Union[BaseModel, dict[str, Any]] = None):
        super().__init__()
        if data is not None:
            self.data = data
        else:
            self.data = {}
        self.message = message
