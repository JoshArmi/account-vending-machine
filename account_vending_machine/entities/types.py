from pydantic import BaseModel


class Configuration(BaseModel):
    base_email: str


class ImportOptions(BaseModel):
    enabled: bool = False
    identifier: str = ""


class AccountRequest(BaseModel):
    name: str
    import_resource: ImportOptions = ImportOptions()


class Account(BaseModel):
    email: str
    name: str
    import_resource: ImportOptions = ImportOptions()
