from subprocess import run as sbrun
from typing import List

import boto3
import click

from account_vending_machine.drivers.terraform_sink import write_resources
from account_vending_machine.drivers.yaml_source import (
    read_accounts,
    read_configuration,
)
from account_vending_machine.entities.types import Account
from account_vending_machine.usecases.accounts import handle_account_request
from account_vending_machine.usecases.organizational_units import (
    handle_organizational_unit_request,
)


def _init():
    sbrun("terraform init", check=True, shell=True, cwd="./bootstrap")


def _workspace_exists(account):
    completed_process = sbrun(
        f"terraform workspace list | grep {account}", shell=True, cwd="./bootstrap"
    )
    return completed_process.returncode == 0


def _create_workspace(account):
    sbrun(
        f"terraform workspace new {account}", check=True, shell=True, cwd="./bootstrap"
    )


def _switch_to_workspace(account):
    sbrun(
        f"terraform workspace select {account}",
        check=True,
        shell=True,
        cwd="./bootstrap",
    )


def _plan(account):
    sbrun(
        f"terraform plan -var target_account_id={account}",
        check=True,
        shell=True,
        cwd="./bootstrap",
    )


def _bootstrap(accounts: List[Account], function):
    _init()
    organizations = boto3.client("organizations")
    paginator = organizations.get_paginator("list_accounts")

    active_accounts = [
        account
        for page in paginator.paginate()
        for account in page["Accounts"]
        if account["Status"] == "ACTIVE"
    ]
    for account in accounts:
        account_id = [
            selected_account
            for selected_account in active_accounts
            if selected_account["Name"] == account.name
        ][0]["Id"]
        if not _workspace_exists(account_id):
            _create_workspace(account_id)
        _switch_to_workspace(account_id)
        function(account_id)


def _apply(account):
    sbrun(
        f"terraform apply -auto-approve -var target_account_id={account}",
        check=True,
        shell=True,
        cwd="./bootstrap",
    )


@click.group()
def run() -> None:
    pass  # pragma: no cover


@run.command()
def plan() -> None:
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
    sbrun("terraform workspace select account-vending-machine", shell=True, check=True)
    sbrun("terraform plan -out=output.tfplan", shell=True, check=True)
    sbrun(
        "terraform show -no-color -json output.tfplan > output.json",
        shell=True,
        check=True,
    )

    _bootstrap(accounts, _plan)


@run.command()
def apply() -> None:
    with open("configuration.yaml", "r") as config_file:
        configuration = read_configuration(config_file.read())
    with open("accounts.yaml", "r") as accounts_file:
        account_requests, _ = read_accounts(accounts_file.read())
    accounts = [
        handle_account_request(configuration, request) for request in account_requests
    ]
    sbrun("terraform init", shell=True, check=True)
    sbrun("terraform workspace select account-vending-machine", shell=True, check=True)
    sbrun("terraform apply -auto-approve output.tfplan", shell=True, check=True)

    _bootstrap(accounts, _apply)
