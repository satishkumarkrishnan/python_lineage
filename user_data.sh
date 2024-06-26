#!/bin/bash   
sudo su -
apt update
apt list --upgradable
apt install -y apache2 
ufw allow 'Apache'
systemctl start apache2
systemctl status apache2
mkdir /var/www/alb
chown -R $USER:$USER /var/www/alb
chmod -R 755 /var/www/alb
echo "<h1>Terraform Learning from $(hostname -f)..</h1>" > /var/www/alb/index.html 
#sleep 600
#yum update -y
#yum install nginx -y
#service nginx start
#echo '<h4> Welcome to AWS</h4>' >> /usr/share/nginx/html/index.html