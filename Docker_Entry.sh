#!/bin/bash

# Detect the operating system
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    echo "Activating virtual environment for Linux"
    source hedral_env/bin/activate
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "Activating virtual environment for macOS"
    source hedral_env/bin/activate
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # Windows
    echo "Activating virtual environment for Windows"
    source hedral_env/Scripts/activate
else
    echo "Unsupported operating system"
    exit 1
fi

# Run the Flask application
python3 src/main/ThreeD_Geometry.py
