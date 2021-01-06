provider "aws" {
  region = var.aws-region
}


terraform {
  backend "s3" {
  bucket = "test-vah-bucket-001"
//  encrypt = true
  key = "main-infra/terraform.tfstate"
  region = "us-east-2"
  dynamodb_table = "terraform-locks-vah-001"
  }
}

//resource "aws_dynamodb_table" "dynamodb-terraform-lock" {
//   name = "terraform-locks-vah-001"
//   hash_key = "LockID"
//   read_capacity = 20
//   write_capacity = 20
//
//   attribute {
//      name = "LockID"
//      type = "S"
//   }
//}

locals {
  web_instance_type_map = {
  stage = "t2.micro"
  prod = "t2.large"
  }
  web_instance_count_map = {
  stage = 1
  prod = 2
  }
  instances = {
  "t2.micro" = data.aws_ami.amazon_linux.id
  "t2.large" = data.aws_ami.amazon_linux.id
  }
}

data "aws_ami" "amazon_linux" {
  owners = ["amazon"]
  most_recent = true
  filter {
    name = "name"
    values = ["amzn-ami-hvm-*-x86_64-gp2"]
  }
  filter {
    name = "owner-alias"
    values = ["amazon"]
  }
}

resource "aws_instance" "instance1" {
  ami = data.aws_ami.amazon_linux.id
  instance_type = local.web_instance_type_map[terraform.workspace]
  count = local.web_instance_count_map[terraform.workspace]
}

resource "aws_instance" "instance2_aka_foreach" {
  for_each = local.instances
  ami = each.value
  instance_type = each.key
  lifecycle {
    create_before_destroy = true
    prevent_destroy = true
  }
}