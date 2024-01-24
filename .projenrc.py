from projen import PythonProject

project = PythonProject(
    author_email="josh.armitage@outlook.com",
    author_name="Josh Armitage",
    module_name="account_vending_machine",
    name="account-vending-machine",
    version="0.1.0",
    dev_deps=["mypy"],
)

project.synth()
