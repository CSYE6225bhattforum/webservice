!#/bin/bash
cd ~
cd webapp
python3 -m venv env
cd env/bin
. activate
cd ../..
pip install -r requirements.txt
python3 app.py
