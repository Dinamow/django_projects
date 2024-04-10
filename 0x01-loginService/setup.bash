#!/usr/bin/env bash

read -s -p "Enter the database password: " db_password
echo -e "\n"
sudo apt update
sudo apt upgrade -y
sudo apt install mysql-server
sudo apt install python3 python3-pip
sudo apt install python3-venv
echo 'CREATE DATABASE IF NOT EXISTS `Djangoapp`' | sudo mysql
echo "CREATE USER IF NOT EXISTS 'Djangouser'@'localhost' IDENTIFIED BY '$db_password'" | sudo mysql
echo "GRANT ALL PRIVILEGES ON Djangoapp.* TO 'Djangouser'@'localhost'" | sudo mysql
echo 'FLUSH PRIVILEGES' | sudo mysql
echo "password=$db_password" > .env
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8000

deactivate