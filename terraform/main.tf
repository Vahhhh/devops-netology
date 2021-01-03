provider "aws" {
  region = "us-east-2"
}

data "aws_ami" "ubuntu" {
  most_recent = true
  owners = ["amazon"]

  filter {
    name = "name"
    values = ["Cloud9Ubuntu-2021-01-01T19-54"]
//    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }
  filter {
    name   = "root-device-type"
    values = ["ebs"]
  }
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

resource "aws_instance" "first_instance" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t2.micro"

  tags = {
    Name = "Temp_tag"
    }
  cpu_core_count = 1
  key_name = "key-1"
}

data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

