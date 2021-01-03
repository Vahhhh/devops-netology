output "account_id" {
  value = data.aws_caller_identity.current.account_id
}

output "caller_user" {
  value = data.aws_caller_identity.current.user_id
}

output "data_region" {
  value = data.aws_region.current
}

output "instance_private_ip_addr" {
  value = aws_instance.first_instance.private_ip
}

output "instance_network_id" {
  value = aws_instance.first_instance.subnet_id
}