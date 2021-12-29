#!/bin/bash

sudo apt update
sudo apt install -y libbluetooth-dev

python3 -m pip install jupyter matplotlib pybluez jupyter_http_over_ws
python3 -m pip install --pre nxt-python

jupyter serverextension enable --py jupyter_http_over_ws

