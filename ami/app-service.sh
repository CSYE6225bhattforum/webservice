#!/bin/bash
cd ~
cd webapp/release
python3 -m venv env
cd env/bin
. activate
cd ../..
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt
python3 app.py

