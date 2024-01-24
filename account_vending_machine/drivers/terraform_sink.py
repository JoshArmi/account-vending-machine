from typing import List

from account_vending_machine.entities.types import (
    Account,
)


def write_resources(accounts: List[Account]) -> None:
    for account in accounts:
        with open("accounts.tf", "w") as file:
            lines = f"""
resource "aws_organizations_account" "{account.name}" {{
    provider = aws.management_account
    name = "{account.name}"
    email = "{account.email}"
    parent_id = data.external.root_id.result.id
    close_on_deletion = true
}}
"""
            file.writelines(lines)
