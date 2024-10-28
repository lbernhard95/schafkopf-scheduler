terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.73.0"
    }
  }
  /*backend "s3" {
    bucket         = "schafkop-scheduler-tf-state-082113759242"
    dynamodb_table = "schafkopf-tf-state-lock"
    key            = "schafkopf-scheduler.tfstate"
    region         = "eu-central-1"
  }*/
}

provider "aws" {
  region = "eu-central-1"
  default_tags {
    tags = {
      application = "Schafkopf Scheduler"
    }
  }
}
