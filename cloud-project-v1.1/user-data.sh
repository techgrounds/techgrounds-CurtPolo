#!/bin/bash

# Update the system
yum update -y

# Install Apache HTTP Server
yum install -y httpd

# Start Apache service
systemctl start httpd

# Enable Apache to start on boot
systemctl enable httpd

# Install mariadb
yum install mariadb -y

# login command
# mysql -h <rds endpoint> -P 3306 -u admin -p

# Install php
yum install php -y