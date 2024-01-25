terraform {
  cloud {
    organization = "Armitagency"

    workspaces {
      name = "account-vending-machine"
    }
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5"
    }
  }
}

provider "aws" {
  region = "ap-southeast-2"
}
