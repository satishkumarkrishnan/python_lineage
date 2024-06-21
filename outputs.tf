output "asg_name" {
  value = aws_autoscaling_group.ddsl_asg.name
}

output "asg_alb_name" {
  value = aws_lb.test.name
}

output "asg_alb_arn" {
  value = aws_lb.test.arn
}

output "asg_alb_dns_name" {
  value = aws_lb.test.dns_name
}

output "asg_policy_arn" {
  value = aws_autoscaling_policy.ddsl_asg_policy.arn
}

output "asg_alb_hosted_zone_id" {
  value = aws_lb.test.zone_id
}

output "private_key" {
  value = aws_launch_template.ddsl_launch_template.name
}

#VPC Outputs
output "vpc_id" {
  value = module.aws_glue.vpc_id
}

output "vpc_fe_subnet" {
  value = module.aws_glue.vpc_fe_subnet
}

output "vpc_be_subnet" {
  value = module.aws_glue.vpc_be_subnet
}

output "vpc_fe_sg" {
  value = module.aws_glue.vpc_fe_sg
}

output "vpc_be_sg" {
  value = module.aws_glue.vpc_be_sg
}

output "vpc_az1" {
  value = module.aws_glue.vpc_az[0]
}

output "vpc_az2" {
  value = module.aws_glue.vpc_az[1]
}

output "vpc_subnet" {
  value = module.aws_glue.vpc_fe_subnet.id
}
