from typing import List

from account_vending_machine.entities.types import (
    Account,
)


def write_resources(accounts: List[Account]) -> None:
    for account in accounts:
        with open("accounts.tf", "w") as file:
            lines = f"""
resource "aws_organizations_account" "{account.name}" {{
    name = "{account.name}"
    email = "{account.email}"
    close_on_deletion = true
}}
"""
            file.writelines(lines)
            if account.import_resource.enabled:
                lines = f"""
import {{
  to = aws_organizations_account.josharmi
  id = "{account.import_resource.identifier}"
}}
"""
            file.writelines(lines)
