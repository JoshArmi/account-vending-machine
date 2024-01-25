from typing import Optional
from pydantic import BaseModel


class Configuration(BaseModel):
    base_email: str


class ImportOptions(BaseModel):
    enabled: bool = False
    identifier: str = ""


class AccountRequest(BaseModel):
    name: str
    email_override: Optional[str] = None
    import_resource: ImportOptions = ImportOptions()


class Account(BaseModel):
    email: str
    name: str
    import_resource: ImportOptions = ImportOptions()


class OrganizationalUnitRequest(BaseModel):
    name: str


class OrganizationalUnit(BaseModel):
    name: str
