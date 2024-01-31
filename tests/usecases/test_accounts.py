from account_vending_machine.entities.types import (
    AccountRequest,
    Configuration,
    ImportOptions,
)
from account_vending_machine.usecases.accounts import handle_account_request

base_config = Configuration(base_email="account-vending-machine@thearmitagency.com")

role_config = Configuration(
    base_email="account-vending-machine@thearmitagency.com",
    role_name="account-vending-machine",
)

base_request = AccountRequest(name="sample-account-preprod")

management_request = AccountRequest(
    name="sample-account-preprod", management_account=True
)

override_request = AccountRequest(
    name="sample-account-preprod", email_override="override@thearmitagency.com"
)

ou_request = AccountRequest(
    name="sample-account-preprod", organizational_unit="Security"
)

import_request = AccountRequest(
    name="sample-account-preprod",
    import_resource=ImportOptions(enabled=True, identifier="941044151014"),
)


def test_handle_account_returns_correct_email():
    assert (
        handle_account_request(base_config, base_request).email
        == "account-vending-machine+sample-account-preprod@thearmitagency.com"
    )


def test_handle_account_returns_correct_role_name():
    assert (
        handle_account_request(role_config, base_request).role_name
        == "account-vending-machine"
    )


def test_handle_management_account_returns_true():
    assert handle_account_request(role_config, management_request).management_account


def test_default_account_returns_no_import():
    assert not handle_account_request(base_config, base_request).import_resource.enabled


def test_handle_account_returns_override_email():
    assert (
        handle_account_request(base_config, override_request).email
        == "override@thearmitagency.com"
    )


def test_handle_account_returns_ou():
    assert (
        handle_account_request(base_config, ou_request).organizational_unit
        == "Security"
    )


def test_import_account_returns_import():
    assert handle_account_request(
        base_config, import_request
    ).import_resource == ImportOptions(enabled=True, identifier="941044151014")
