from account_vending_machine.entities.types import (
    Account,
    AccountRequest,
    Configuration,
)


def handle_account_request(config: Configuration, request: AccountRequest) -> Account:
    tokens = config.base_email.split("@")
    email = tokens[0] + "+" + request.name + "@" + tokens[1]
    return Account(
        email=email if not request.email_override else request.email_override,
        name=request.name,
        import_resource=request.import_resource,
        organizational_unit=request.organizational_unit
        if request.organizational_unit
        else None,
        role_name=config.role_name if config.role_name else None,
        management_account=request.management_account,
    )
