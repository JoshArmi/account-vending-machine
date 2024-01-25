from json import loads
from os import path, remove
import pprint
from shutil import copy, move

from pytest import fixture, mark

from account_vending_machine.entrypoints import run


def set_up_files():
    remove("./terraform.tf.back") if path.exists("./terraform.tf.back") else None
    move("./terraform.tf", "./terraform.tf.back")
    copy("./tests/entrypoints/terraform.tf", "./terraform.tf")
    remove("./accounts.yaml.back") if path.exists("./accounts.yaml.back") else None
    move("./accounts.yaml", "./accounts.yaml.back")
    copy("./tests/entrypoints/accounts.yaml", "./accounts.yaml")
    remove("./configuration.yaml.back") if path.exists(
        "./configuration.yaml.back"
    ) else None
    move("./configuration.yaml", "./configuration.yaml.back")
    copy("./tests/entrypoints/configuration.yaml", "./configuration.yaml")
    remove("./.terraform/terraform.tfstate") if path.exists(
        "./.terraform/terraform.tfstate"
    ) else None


def clean_up_files():
    move("./terraform.tf.back", "./terraform.tf")
    move("./accounts.yaml.back", "./accounts.yaml")
    move("./configuration.yaml.back", "./configuration.yaml")
    remove("./output.tfplan")
    remove("./output.json")
    remove("./.terraform/terraform.tfstate") if path.exists(
        "./.terraform/terraform.tfstate"
    ) else None


@fixture(autouse=True, scope="session")
def run_main_loop():
    set_up_files()
    run()
    yield {}
    clean_up_files()


def expected_change_exists(changes, type, name, actions) -> bool:
    for change in changes:
        if (
            change["type"] == type
            and change["name"] == name
            and change["change"]["actions"] == actions
        ):
            return True
    return False


@mark.integration
def test_run_plans_to_create_account():
    with open("output.json", "r") as file:
        resource_changes = loads(file.read())["resource_changes"]
        assert expected_change_exists(
            resource_changes,
            "aws_organizations_account",
            "joshs-test-account-2",
            ["create"],
        )


@mark.integration
def test_run_plans_to_create_organizational_units():
    with open("output.json", "r") as file:
        resource_changes = loads(file.read())["resource_changes"]
        pprint.pprint(resource_changes)
        assert expected_change_exists(
            resource_changes,
            "aws_organizations_organizational_unit",
            "Workloads",
            ["create"],
        ), "Organizational Unit Workloads not found"
