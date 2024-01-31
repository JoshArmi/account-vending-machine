from typing import List, Tuple
from yaml import load, Loader

from account_vending_machine.entities.types import (
    AccountRequest,
    Configuration,
    ImportOptions,
    OrganizationalUnitRequest,
)


def read_accounts(
    accounts_input: str,
) -> Tuple[List[AccountRequest], List[OrganizationalUnitRequest]]:
    yaml = load(accounts_input, Loader)
    accounts = (
        [
            AccountRequest(
                name=account["name"],
                email_override=account["email_override"]
                if "email_override" in account.keys()
                else None,
                import_resource=ImportOptions(
                    enabled=True,
                    identifier=account["import"]["id"],
                )
                if "import" in account.keys()
                else ImportOptions(),
                management_account=account["management_account"]
                if "management_account" in account.keys()
                else False,
            )
            for account in yaml["accounts"]
        ]
        if "accounts" in yaml.keys()
        else []
    )
    organizational_units = (
        [
            OrganizationalUnitRequest(name=organizational_unit)
            for organizational_unit in yaml["organizational_units"]
        ]
        if "organizational_units" in yaml.keys()
        else []
    )
    return (accounts, organizational_units)


def read_configuration(configuration_input: str) -> Configuration:
    yaml = load(configuration_input, Loader)
    return Configuration(
        base_email=yaml["base_email"],
        role_name=yaml["role_name"] if "role_name" in yaml.keys() else None,
    )
