#!/bin/bash

# Create a virtual environment named sqlagent
echo "Creating virtual environment..."
python3 -m venv .venv

# Activate the virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install libraries from requirements.txt 
echo "Installing libraries from requirements.txt..."
pip install -r requirements.txt

# Copy env backup to .env file
if [ -f ".env.example" ]; then
    echo "Copying env.example to .env..."
    cp env.example .env
else
    echo "No .env.example file found. Creating a new .env file..."
    touch .env
fi

composio add youtube

composio add notion
