from pydantic import BaseModel


class ResponseModel(BaseModel):
    status: str


class RequestProductModel(BaseModel):
    shop_id: int
    file_name: str
