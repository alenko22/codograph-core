#!/bin/bash
# Обновляем список пакетов и устанавливаем Graphviz
apt-get update
apt-get install -y graphviz

# Устанавливаем Python-зависимости
pip install -r requirements.txt