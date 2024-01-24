from account_vending_machine.entities.types import (
    Account,
    AccountRequest,
    Configuration,
)


def handle_account_request(config: Configuration, request: AccountRequest) -> Account:
    tokens = config.base_email.split("@")
    email = tokens[0] + "+" + request.name + "@" + tokens[1]
    return Account(
        email=email, name=request.name, import_resource=request.import_resource
    )
