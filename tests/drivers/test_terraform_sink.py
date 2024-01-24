import hcl2
from account_vending_machine.drivers.terraform_sink import write_resources
from account_vending_machine.entities.types import Account, ImportOptions


def test_outputs_account_to_file():
    write_resources(
        accounts=[
            Account(
                email="my-special-account@thearmitagency.com",
                name="my-special-account",
            )
        ]
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
        ]
    )
    with open("accounts.tf") as file:
        imports = hcl2.load(file)["import"]
        for i in imports:
            if i == {
                "to": "${aws_organizations_account.josharmi}",
                "id": "941044151014",
            }:
                return
    raise Exception("Did not find expected Terraform resource")
