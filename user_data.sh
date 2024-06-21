#!/bin/bash   
sudo su -
apt update
apt list --upgradable
apt install apache2 -y  
ufw allow 'Apache'
systemctl start apache2
systemctl status apache2
mkdir /var/www/alb
chown -R $USER:$USER /var/www/alb
chmod -R 755 /var/www/alb
#sudo echo "<h4>Terraform Learning from $(hostname -f)..</h4>" > /usr/share/nginx/html/index.html
echo "<h1>Terraform Learning from $(hostname -f)..</h1>" > /var/www/alb/index.html