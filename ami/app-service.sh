# !/bin/bash
# cd ~
# cd webapp/
# python3 -m venv env
# cd env/bin
# . activate
# cd ../..
cd ~
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt
cd webservice-0.0.1/
python3 app.py
