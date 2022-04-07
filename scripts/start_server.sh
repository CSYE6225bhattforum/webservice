#!/bin/bash
#sudo tar -xvz --overwrite /home/ec2-user/webservice-0.0.1.tar.gz -C /home/ec2-user/
sudo tar xvzf /home/ec2-user/webservice-0.0.1.tar.gz -C /home/ec2-user/
cd /home/ec2-user/webservice-0.0.1
pip3 install -r /home/ec2-user/requirements.txt