#!/bin/bash   
# sudo apt update
# sudo apt list --upgradable
# sudo apt install -y apache2 
# sudo ufw allow 'Apache'
# sudo systemctl start apache2
# sudo systemctl status apache2
# sudo mkdir /var/www/alb
# sudo chown -R $USER:$USER /var/www/alb
# sudo chmod -R 755 /var/www/alb
# #sudo echo "<h4>Terraform Learning from $(hostname -f)..</h4>" > /usr/share/nginx/html/index.html
# sudo echo "<h1>Terraform Learning from $(hostname -f)..</h1>" > /var/www/alb/index.html
sudo su - 
sleep 600
yum update -y
yum install nginx -y
service nginx start
echo '<h4> Welcome to AWS</h4>' >> /usr/share/nginx/html/index.html