#!/bin/bash

sudo su -c 'echo "deb http://www.rabbitmq.com/debian/ testing main" >> /etc/apt/sources.list'
curl http://www.rabbitmq.com/rabbitmq-signing-key-public.asc | sudo apt-key add -

#echo 'deb http://www.rabbitmq.com/debian/ testing main' | sudo tee -a /etc/apt/sources.list
sudo apt-get update
#wget http://www.rabbitmq.com/rabbitmq-signing-key-public.asc
#sudo apt-key add rabbitmq-signing-key-public.asc
sudo apt-get install -y --force-yes rabbitmq-server
sudo /usr/lib/rabbitmq/bin/rabbitmq-plugins enable rabbitmq_management
sudo service rabbitmq-server restart
rabbitmqctl add_user test test
rabbitmqctl set_user_tags test administrator
rabbitmqctl set_permissions -p / test ".*" ".*" ".*"

sudo apt-get install -y python-pip
sudo pip install pika
