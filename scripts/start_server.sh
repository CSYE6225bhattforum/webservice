#!/bin/bash
sudo tar xvzf /home/ec2-user/dist/webservice-0.0.1.tar.gz -C /home/ec2-user/
cd /home/ec2-user/webservice-0.0.1
# sudo pip3 install -e .
pip3 install -r /home/ec2-user/requirements.txt
sudo systemctl daemon-reload
sudo systemctl enable webservice.service
sudo systemctl start webservice.service
sudo systemctl status webservice.service