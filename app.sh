#!/bin/bash

git pull
source /opt/minRigs-Marine/venv/bin/activate
pip install -r requirements.txt
python /opt/minRigs-Marine/app/barendBoot.py