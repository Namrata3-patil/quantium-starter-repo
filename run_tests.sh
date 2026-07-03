#!/bin/bash

# 1. Navigate to the script's directory location
cd "$(dirname "$0")"

# 2. Activate the virtual environment
# (Using the standard POSIX path compatibility layout for the environment)
if [ -d "./venv/Scripts" ]; then
    source ./venv/Scripts/activate
elif [ -d "./venv/bin" ]; then
    source ./venv/bin/activate
else
    echo "Error: Virtual environment (venv) not found!"
    exit 1
fi

echo "Virtual environment activated successfully. Running test suite..."

# 3. Execute the test suite with the custom plugin bypass flag
pytest -p no:dash test_app.py

# 4. Check the exit status of the pytest command
# $? captures the return code of the last executed process automatically
if [ $? -eq 0 ]; then
    echo "Success: All automated regression verification checkpoints passed!"
    exit 0
else
    echo "Failure: Test suite verification execution encountered an anomaly."
    exit 1
fi