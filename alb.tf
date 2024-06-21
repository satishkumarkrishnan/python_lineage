
# To create ALB
resource "aws_lb" "test" {
  internal                   = false
  name                       = "ddsl-alb"
  load_balancer_type         = "application"
  security_groups = [module.aws_glue.vpc_fe_sg, module.aws_glue.vpc_be_sg]
  subnets      = [module.aws_glue.vpc_fe_subnet.id, module.aws_glue.vpc_be_subnet.id]
  enable_deletion_protection = false
  
}
# Target Group Creation
resource "aws_lb_target_group" "target-group" {
  name        = "ddsl-lb-tg"
  port        = 5000
  protocol    = "HTTP"
  target_type = "instance"  
  vpc_id      = module.aws_glue.vpc_id  

  health_check {
    enabled             = true
    interval            = 10
    path                = "/"
    port                = "traffic-port"
    protocol            = "HTTP"
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }
  tags = {
    Environment = "dev"
  }
}
#ALB Listener
resource "aws_lb_listener" "alb-listener" {
  load_balancer_arn = aws_lb.test.arn
  port              = 5000
  protocol          = "HTTP"
  depends_on        = [aws_lb_target_group.target-group]

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.target-group.arn
    fixed_response {
      content_type = "text/plain"
      message_body = "404: page not found"
      status_code  = 404
    }
  }
}

resource "aws_autoscaling_attachment" "asg_attachment" {
 autoscaling_group_name = aws_autoscaling_group.ddsl_asg.name
 lb_target_group_arn   = aws_lb_target_group.target-group.arn
 }