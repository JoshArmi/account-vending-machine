from account_vending_machine.entities.types import (
    AccountRequest,
    Configuration,
    ImportOptions,
)
from account_vending_machine.usecases.accounts import handle_account_request

base_config = Configuration(base_email="apac-scaffolding-aws@contino.io")

base_request = AccountRequest(name="sample-account-preprod")

import_request = AccountRequest(
    name="sample-account-preprod",
    import_resource=ImportOptions(enabled=True, identifier="941044151014"),
)


def test_handle_account_returns_correct_email():
    assert (
        handle_account_request(base_config, base_request).email
        == "apac-scaffolding-aws+sample-account-preprod@contino.io"
    )


def test_default_account_returns_no_import():
    assert not handle_account_request(base_config, base_request).import_resource.enabled


def test_import_account_returns_import():
    assert handle_account_request(
        base_config, import_request
    ).import_resource == ImportOptions(enabled=True, identifier="941044151014")
