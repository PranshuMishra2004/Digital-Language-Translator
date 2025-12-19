#!/bin/bash

echo "Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Error installing dependencies. Make sure pip is installed."
    exit 1
fi

echo ""
echo "Starting Flask server..."
echo "Server will run on http://localhost:5000"
echo ""
echo "Open index.html in your browser to use the application."
echo "Press Ctrl+C to stop the server."
echo ""

python app.py

