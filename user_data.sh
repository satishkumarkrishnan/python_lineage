#!/bin/bash   
sudo apt update
#sudo apt list --upgradable
#sudo apt install apache2 -y  
#sudo ufw allow 'Apache'
#sudo systemctl status apache2
#sudo mkdir /var/www/alb
sudo yum update -y
sudo yum install nginx -y
sudo service nginx start
#sudo chown -R $USER:$USER /var/www/alb
#sudo chmod -R 755 /var/www/alb
sudo echo "<h4>Terraform Learning from $(hostname -f)..</h4>" > /usr/share/nginx/html/index.html