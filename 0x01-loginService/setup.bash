#!/usr/bin/env bash

sudo apt update
sudo apt upgrade -y
sudo apt install mysql-server
sudo apt install python3 python3-pip
sudo apt install python3-venv
echo 'CREATE DATABASE IF NOT EXISTS `Djangoapp`' | sudo mysql
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8000

deactivate