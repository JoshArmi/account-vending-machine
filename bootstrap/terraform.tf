

terraform {
  cloud {
    organization = "Armitagency"

    workspaces {
      tags = ["account-vending-machine"]
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

provider "aws" {
  alias  = "target"
  region = "ap-southeast-2"
  assume_role {
    role_arn = "arn:aws:iam::${var.target_account_id}:role/account-vending-machine"
  }
}

variable "target_account_id" {
  type = string
}
