#!/bin/bash   
sudo su - 
apt update
apt list --upgradable
apt install apache2    
ufw allow 'Apache'
systemctl status apache2
mkdir /var/www/alb
chown -R $USER:$USER /var/www/alb
chmod -R 755 /var/www/alb
echo "<h1>Terraform Learning from $(hostname -f)..</h1>" > /var/www/alb/index.html