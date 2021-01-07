provider "aws" {
  region = "eu-east-2"
}

data "aws_ami" "amazon_linux" {
  most_recent = true
  owners = ["amazon"]
  filter {
    name = "name"
    values = [
      "amzn-ami-hvm-*-x86_64-gp2",
    ]
  }
  filter {
    name = "owner-alias"
    values = [
      "amazon",
    ]
  }
}


module "ec2-instance-stage" {
  source  = "terraform-aws-modules/ec2-instance/aws"
  version = "2.16.0"
  ami = data.aws_ami.amazon_linux.id
  instance_type = "t2.micro"
  name = "instance from module ec2"
  instance_count = 1
  tags = {
    Terraform   = "true"
    Environment = "stage"
  }
}

module "ec2-instance-prod" {
  source  = "terraform-aws-modules/ec2-instance/aws"
  version = "2.16.0"
  ami = data.aws_ami.amazon_linux.id
  instance_type = "t2.large"
  name = "instance from module ec2"
  instance_count = 2
  tags = {
    Terraform   = "true"
    Environment = "prod"
  }
}