from account_vending_machine.entities.types import (
    OrganizationalUnitRequest,
    OrganizationalUnit,
)


def handle_organizational_unit_request(
    request: OrganizationalUnitRequest,
) -> OrganizationalUnit:
    return OrganizationalUnit(name=request.name)
