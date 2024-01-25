import hcl2
from account_vending_machine.drivers.terraform_sink import write_resources
from account_vending_machine.entities.types import (
    Account,
    ImportOptions,
    OrganizationalUnit,
)


def test_outputs_account_to_file():
    write_resources(
        accounts=[
            Account(
                email="my-special-account@thearmitagency.com",
                name="my-special-account",
            )
        ],
        organizational_units=[],
    )
    with open("accounts.tf") as file:
        resources = hcl2.load(file)["resource"]
        for resource in resources:
            print(resource)
            if resource == {
                "aws_organizations_account": {
                    "my-special-account": {
                        "name": "my-special-account",
                        "email": "my-special-account@thearmitagency.com",
                        "parent_id": "${data.external.root_id.result.id}",
                        "close_on_deletion": True,
                    }
                }
            }:
                return
    raise Exception("Did not find expected Terraform resource")


def test_outputs_account_ou_to_file():
    write_resources(
        accounts=[
            Account(
                email="my-special-account@thearmitagency.com",
                name="my-special-account",
                organizational_unit="Security",
            )
        ],
        organizational_units=[],
    )
    with open("accounts.tf") as file:
        resources = hcl2.load(file)["resource"]
        for resource in resources:
            print(resource)
            if resource == {
                "aws_organizations_account": {
                    "my-special-account": {
                        "name": "my-special-account",
                        "email": "my-special-account@thearmitagency.com",
                        "parent_id": "${aws_organizations_organizational_unit.Security.id}",
                        "close_on_deletion": True,
                    }
                }
            }:
                return
    raise Exception("Did not find expected Terraform resource")


def test_outputs_account_with_space():
    write_resources(
        accounts=[
            Account(
                email="my-special-account@thearmitagency.com",
                name="Super Account",
            )
        ],
        organizational_units=[],
    )
    with open("accounts.tf") as file:
        resources = hcl2.load(file)["resource"]
        for resource in resources:
            print(resource)
            if resource == {
                "aws_organizations_account": {
                    "Super_Account": {
                        "name": "Super Account",
                        "email": "my-special-account@thearmitagency.com",
                        "parent_id": "${data.external.root_id.result.id}",
                        "close_on_deletion": True,
                    }
                }
            }:
                return
    raise Exception("Did not find expected Terraform resource")


def test_outputs_account_import_to_file():
    write_resources(
        accounts=[
            Account(
                email="my-special-account@thearmitagency.com",
                name="my-special-account",
                import_resource=ImportOptions(enabled=True, identifier="941044151014"),
            )
        ],
        organizational_units=[],
    )
    with open("accounts.tf") as file:
        imports = hcl2.load(file)["import"]
        for i in imports:
            if i == {
                "to": "${aws_organizations_account.my-special-account}",
                "id": "941044151014",
            }:
                return
    raise Exception("Did not find expected Terraform resource")


def test_outputs_organizational_units_to_file():
    write_resources([], organizational_units=[OrganizationalUnit(name="Security")])
    with open("accounts.tf") as file:
        resources = hcl2.load(file)["resource"]
        for resource in resources:
            if resource == {
                "aws_organizations_organizational_unit": {
                    "Security": {
                        "name": "Security",
                        "parent_id": "${data.external.root_id.result.id}",
                    }
                }
            }:
                return

    raise Exception("Did not find expected Terraform resource")


def test_outputs_organizational_units_with_space():
    write_resources(
        [], organizational_units=[OrganizationalUnit(name="Policy Staging")]
    )
    with open("accounts.tf") as file:
        resources = hcl2.load(file)["resource"]
        for resource in resources:
            if resource == {
                "aws_organizations_organizational_unit": {
                    "Policy_Staging": {
                        "name": "Policy Staging",
                        "parent_id": "${data.external.root_id.result.id}",
                    }
                }
            }:
                return

    raise Exception("Did not find expected Terraform resource")


def test_outputs_data_org_root_id_script_to_file():
    write_resources(
        accounts=[],
        organizational_units=[],
    )
    with open("accounts.tf") as file:
        data = hcl2.load(file)["data"]
        for datum in data:
            if datum == {"external": {"root_id": {"program": ["./get_root_id.sh"]}}}:
                return

    raise Exception("Did not find expected Terraform resource")
