from projen import ProjectType
from projen.python import PythonProject

project = PythonProject(
    author_email="josh.armitage@outlook.com",
    author_name="Josh Armitage",
    deps=["pydantic", "python-hcl2", "pyyaml", "types-pyyaml", "boto3", "click"],
    dev_deps=[
        "black",
        "mypy",
        "pytest",
        "pytest-cov",
        "pytest-watch",
        "boto3-stubs[organizations]",
    ],
    module_name="account_vending_machine",
    name="account-vending-machine",
    project_type=ProjectType.APP,
    version="0.1.0",
)

project.add_task("watch", exec="ptw -- -m 'not integration'")
project.add_task("plan", exec="python -m account_vending_machine plan")
project.add_task(
    "apply",
    exec="python -m account_vending_machine plan",
)

project.add_git_ignore("accounts.tf")
project.add_git_ignore("*.tfstate")
project.add_git_ignore("*.tfstate.*")
project.add_git_ignore("**/.terraform/*")
project.add_git_ignore("output.json")
project.add_git_ignore("output.tfplan")

project.synth()
