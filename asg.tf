#Terraform resource for key pair
resource "aws_key_pair" "deployer" {
  key_name   = "ec2-key"
  public_key = file("${path.module}/key")
}
#Terraform Launch Template Resource creation
resource "aws_launch_template" "ddsl_launch_template" {
  #count         = 2
  name_prefix   = "ddsl_asg"
  image_id      = var.ami
  instance_type = var.instance_type
  #user_data     = filebase64("${path.module}/user_data.sh")
  user_data     = "${filebase64("user_data.sh")}"
  key_name      = "ec2-key"
  vpc_security_group_ids = [module.aws_glue.vpc_fe_sg]    
  tag_specifications {
    resource_type = "instance"

    tags = {
      Name = "ddsl_lineage"
    }
  } 
 
}
#Terraform ASG Resource creation
resource "aws_autoscaling_group" "ddsl_asg" {
  desired_capacity       = var.desired_capacity
  max_size               = var.max_size
  min_size               = var.min_size
  health_check_type      = "EC2"
  vpc_zone_identifier    = [module.aws_glue.vpc_fe_subnet.id, module.aws_glue.vpc_be_subnet.id]
  launch_template {
      id      = aws_launch_template.ddsl_launch_template.id      
      version = "$Latest"
    } 
}
#Terraform ASG policy Resource creation
 resource "aws_autoscaling_policy" "ddsl_asg_policy" {
  name                   = "ddsl-asg-policy"
  scaling_adjustment     = 4
  adjustment_type        = "ChangeInCapacity"
  cooldown               = 300
  autoscaling_group_name = aws_autoscaling_group.ddsl_asg.name  
}