#!/bin/bash

source venv/bin/activate

sudo systemctl start mariadb
while ! mysqladmin ping -h localhost --silent; do
    sleep 2
done
# Wait database server to start

# Launch
python main.py