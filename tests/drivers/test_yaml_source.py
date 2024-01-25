from account_vending_machine.drivers.yaml_source import (
    read_accounts,
    read_configuration,
)
from account_vending_machine.entities.types import (
    AccountRequest,
    Configuration,
    ImportOptions,
    OrganizationalUnitRequest,
)


def test_handles_configuration():
    example_yaml = """
base_email: josh@thearmitagency.com
"""
    assert read_configuration(example_yaml) == Configuration(
        base_email="josh@thearmitagency.com"
    )


def test_correctly_translates_account_definition():
    example_yaml = """
accounts:
  - name: test-account
"""
    assert read_accounts(example_yaml)[0] == [
        AccountRequest(
            name="test-account",
        )
    ]


def test_correctly_translates_override_account_definition():
    example_yaml = """
accounts:
  - name: test-account
    email_override: override@thearmitagency.com
"""
    assert read_accounts(example_yaml)[0] == [
        AccountRequest(
            name="test-account", email_override="override@thearmitagency.com"
        )
    ]


def test_correctly_translates_import_account_definition():
    example_yaml = """
accounts:
  - name: test-account
    import:
        id: 012345678912
"""
    assert read_accounts(example_yaml)[0] == [
        AccountRequest(
            name="test-account",
            import_resource=ImportOptions(enabled=True, identifier="012345678912"),
        )
    ]


def test_correctly_translates_organizational_units_definition():
    example_yaml = """
organizational_units:
  - Workloads
  - Security
"""
    assert read_accounts(example_yaml)[1] == [
        OrganizationalUnitRequest(
            name="Workloads",
        ),
        OrganizationalUnitRequest(
            name="Security",
        ),
    ]
