#!/bin/bash

source venv/bin/activate

sudo systemctl start mariadb
while ! mysqladmin ping -h localhost --silent; do
    sleep 1
done
sleep 2
# Wait database server to start

# Launch API
python main.py