#!/bin/bash

pip install python-telegram-bot google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
pip3 install python-telegram-bot google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

SERVICE_NAME=telegram_google_integration
WORKING_DIR=$(pwd)
SCRIPT_NAME=main.py

# Create service file
echo "[Unit]
Description=My Python Application
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$WORKING_DIR
ExecStart=python3 $WORKING_DIR/$SCRIPT_NAME
Restart=on-failure
RestartSec=15

[Install]
WantedBy=multi-user.target" > /etc/systemd/system/$SERVICE_NAME.service

# Reload systemd manager configuration
systemctl daemon-reload

# Enable service
systemctl enable $SERVICE_NAME

# Start service
systemctl start $SERVICE_NAME

echo systemctl status $SERVICE_NAME