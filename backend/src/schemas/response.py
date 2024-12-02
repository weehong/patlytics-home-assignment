from pydantic import BaseModel


class CompanyResponse(BaseModel):
    message: str
    data: dict
    status: bool
