#!/bin/bash

sudo apt install python3-gi gir1.2-webkit2-4.0 -y

git pull
source /opt/minRigs-Marine/venv/bin/activate
pip install -r requirements.txt
python /opt/minRigs-Marine/app/barendBoot.py