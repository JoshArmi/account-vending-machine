from typing import Optional
from pydantic import BaseModel


class Configuration(BaseModel):
    base_email: str
    role_name: Optional[str] = None


class ImportOptions(BaseModel):
    enabled: bool = False
    identifier: str = ""


class AccountRequest(BaseModel):
    name: str
    email_override: Optional[str] = None
    import_resource: ImportOptions = ImportOptions()
    organizational_unit: Optional[str] = None
    management_account: bool = False


class Account(BaseModel):
    email: str
    name: str
    import_resource: ImportOptions = ImportOptions()
    organizational_unit: Optional[str] = None
    role_name: Optional[str] = None
    management_account: bool = False


class OrganizationalUnitRequest(BaseModel):
    name: str


class OrganizationalUnit(BaseModel):
    name: str
