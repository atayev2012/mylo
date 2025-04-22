from pydantic import BaseModel, Field

class WebApplication(BaseModel):
    service_type: str = Field(examples=["Брендинг"])
    client_type: str = Field(examples=["недвижимость"])
    budget_type: str = Field(examples=["до 50 000"])
    deadline_type: str = Field(examples=["1 месяц"])
    name: str = Field(examples=["Дмитрий"])
    phone: str = Field(examples=["+79996669966"])
    email: str = Field(examples=["dimka@mail.ru"])
    comment: str | None = Field(examples=["новый бренд в минимализме"])





