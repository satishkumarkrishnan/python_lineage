#!/bin/bash   
sudo apt update
sudo apt list --upgradable
sudo apt install apache2    
sudo ufw allow 'Apache'
sudo systemctl status apache2
sudo mkdir /var/www/alb
sudo chown -R $USER:$USER /var/www/alb
sudo chmod -R 755 /var/www/alb
sudo echo "<h1>Terraform Learning from $(hostname -f)..</h1>" > /var/www/alb/index.html