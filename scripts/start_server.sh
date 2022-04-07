#!/bin/bash
#sudo tar -xvz --overwrite /home/ec2-user/webservice-0.0.1.tar.gz -C /home/ec2-user/
sudo tar xvzf /home/ec2-user/webservice-0.0.1.tar.gz -C /home/ec2-user/
cd /home/ec2-user/webservice-0.0.1
pip3 install -r /home/ec2-user/requirements.txt
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -c file:/opt/cloudwatch-config.json -s
