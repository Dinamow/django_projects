#!/usr/bin/env bash
if [ -f .env ]; then
    echo "migration already done"
else
    read -s -p "Enter the database password: " db_password
    echo -e "\n"
    sudo apt update
    sudo apt upgrade -y
    sudo apt install mysql-server -y
    sudo apt install python3 python3-pip -y
    sudo apt install python3-venv -y
    echo 'CREATE DATABASE IF NOT EXISTS `Djangoapp`' | sudo mysql
    echo 'CREATE DATABASE IF NOT EXISTS `Djangoapp_test`' | sudo mysql
    echo "CREATE USER IF NOT EXISTS 'Djangouser'@'localhost' IDENTIFIED BY '$db_password'" | sudo mysql
    echo "GRANT ALL PRIVILEGES ON Djangoapp_test.* TO 'Djangouser'@'localhost'" | sudo mysql
    echo "GRANT ALL PRIVILEGES ON Djangoapp.* TO 'Djangouser'@'localhost'" | sudo mysql
    echo 'FLUSH PRIVILEGES' | sudo mysql
    echo "password=$db_password" > .env
    pip3 install -r requirements.txt
fi
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8000
