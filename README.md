# Account Vending Machine

This repository is an example of a YAML -> Python -> Terraform AWS Account Vending Machine.

To understand why this pattern exists, and why I prefer it to straight Terraform or ServiceNow centric implementations please [read this](https://medium.com/@josh.armitage/aws-account-vending-machines-a7749b577fb9).

## Using The Account Vending Machine

First assume a sufficiently privileged role in your root account. (I'd suggest using [granted](https://www.granted.dev/))

### To see what changes will be made:

```bash
npx projen
```

### To apply changes:

```bash
npx projen apply
```

## Building This Project

This project uses [projen](https://projen.io) for configuration management.

