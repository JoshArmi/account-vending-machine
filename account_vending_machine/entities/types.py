from pydantic import BaseModel


class Configuration(BaseModel):
    base_email: str


class AccountRequest(BaseModel):
    name: str


class Account(BaseModel):
    email: str
    name: str
