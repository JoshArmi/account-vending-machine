from subprocess import run as sbrun

from account_vending_machine.drivers.terraform_sink import write_resources
from account_vending_machine.drivers.yaml_source import (
    read_accounts,
    read_configuration,
)
from account_vending_machine.usecases.accounts import handle_account_request
from account_vending_machine.usecases.organizational_units import (
    handle_organizational_unit_request,
)


def run() -> None:
    with open("configuration.yaml", "r") as config_file:
        configuration = read_configuration(config_file.read())
    with open("accounts.yaml", "r") as accounts_file:
        account_requests, organizational_units_requests = read_accounts(
            accounts_file.read()
        )
    accounts = [
        handle_account_request(configuration, request) for request in account_requests
    ]
    organizational_units = [
        handle_organizational_unit_request(request)
        for request in organizational_units_requests
    ]
    write_resources(accounts, organizational_units)
    sbrun("terraform init", shell=True, check=True)
    sbrun("terraform plan -out=output.tfplan", shell=True, check=True)
    sbrun(
        "terraform show -no-color -json output.tfplan > output.json",
        shell=True,
        check=True,
    )
