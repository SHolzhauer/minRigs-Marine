#!/bin/bash

git pull
source /opt/minRigs-Marine/venv/bin/activate
pip install -r requirements.txt
chmod +x venv/bin/garden
garden install mapview
python /opt/minRigs-Marine/app/barendBoot.py