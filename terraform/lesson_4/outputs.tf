output "ids_stage" {
  description = "List of IDs of STAGE instances"
  value       = module.ec2-instance-stage.id
}

output "ids_prod" {
  description = "List of IDs of PROD instances"
  value       = module.ec2-instance-prod.id
}
