from account_vending_machine.entities.types import (
    OrganizationalUnit,
    OrganizationalUnitRequest,
)
from account_vending_machine.usecases.organizational_units import (
    handle_organizational_unit_request,
)


def test_handle_organizational_unit_returns_correct_object():
    assert handle_organizational_unit_request(
        OrganizationalUnitRequest(name="Workloads")
    ) == OrganizationalUnit(name="Workloads")
