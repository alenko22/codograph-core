#!/bin/bash
apt-get update
apt-get install -y graphviz
pip install -r requirements.txt
python manage.py collectstatic --noinput