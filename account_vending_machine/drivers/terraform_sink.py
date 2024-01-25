from subprocess import run
from typing import List

from account_vending_machine.entities.types import (
    Account,
    OrganizationalUnit,
)


def _massage_string_for_terraform(string: str) -> str:
    return (
        string.replace(".", "_").replace("@", "-").replace("+", "-").replace(" ", "_")
    )


def write_resources(
    accounts: List[Account], organizational_units: List[OrganizationalUnit]
) -> None:
    with open("accounts.tf", "w") as file:
        for account in accounts:
            lines = f"""
resource "aws_organizations_account" "{_massage_string_for_terraform(account.name)}" {{
    name = "{account.name}"
    email = "{account.email}"
    parent_id = {f"aws_organizations_organizational_unit.{_massage_string_for_terraform(account.organizational_unit)}.id" if account.organizational_unit else "data.external.root_id.result.id"}
    close_on_deletion = true
}}
"""
            file.writelines(lines)
            if account.import_resource.enabled:
                lines = f"""
import {{
  to = aws_organizations_account.{_massage_string_for_terraform(account.name)}
  id = "{account.import_resource.identifier}"
}}
"""
                file.writelines(lines)

        for organizational_unit in organizational_units:
            lines = f"""
resource "aws_organizations_organizational_unit" "{_massage_string_for_terraform(organizational_unit.name)}" {{
    name = "{organizational_unit.name}"
    parent_id = data.external.root_id.result.id
}}
"""
            file.writelines(lines)

        lines = """
data "external" "root_id" {
    program = ["./get_root_id.sh"]
}
"""
        file.writelines(lines)

    run("terraform fmt", shell=True)
