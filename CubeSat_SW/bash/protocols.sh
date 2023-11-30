#!/bin/bash

chmod +x protocols.sh
chmod +x ../Optimization.py

# System dependencies
sudo apt-get update
sudo apt-get install -y python3 python3-pip i2c-tools

# Enable I2C and SPI
sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_spi 0

