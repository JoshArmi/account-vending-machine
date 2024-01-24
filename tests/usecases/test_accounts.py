from account_vending_machine.entities.types import AccountRequest, Configuration
from account_vending_machine.usecases.accounts import handle_account_request

base_config = Configuration(base_email="apac-scaffolding-aws@contino.io")

base_request = AccountRequest(
    name="sample-account-preprod",
)


def test_handle_account_returns_correct_email():
    assert (
        handle_account_request(base_config, base_request).email
        == "apac-scaffolding-aws+sample-account-preprod@contino.io"
    )
