import hcl2
from account_vending_machine.drivers.terraform_sink import write_resources
from account_vending_machine.entities.types import Account


def test_outputs_account_to_file():
    write_resources(
        accounts=[
            Account(
                email="my-special-account@thearmitagency.com", name="my-special-account"
            )
        ]
    )
    with open("accounts.tf") as file:
        resources = hcl2.load(file)["resource"]
        for resource in resources:
            if resource == {
                "aws_organizations_account": {
                    "my-special-account": {
                        "provider": "${aws.management_account}",
                        "name": "my-special-account",
                        "email": "my-special-account@thearmitagency.com",
                        "parent_id": "${data.external.root_id.result.id}",
                        "close_on_deletion": True,
                    }
                }
            }:
                return
    raise Exception("Did not find expected Terraform resource")
